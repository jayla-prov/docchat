"""Chat about local documents using manual and model requested tools."""
import argparse
import json
import shlex

from tools.compact import compact
from tools.calculate import calculate
from tools.cat import cat
from tools.grep import grep
from tools.ls import ls
import os
from dotenv import load_dotenv
from groq import Groq

functions = {
    'calculate': calculate,
    'ls': ls,
    'cat': cat,
    'grep': grep,
}

tools = [
    {
        'type': 'function',
        'function': {
            'name': 'calculate',
            'description': 'Evaluate an arithmetic expression.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'expression': {'type': 'string'},
                },
                'required': ['expression'],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'ls',
            'description': 'List the contents of a relative folder.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'path': {'type': 'string'},
                },
                'required': [],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'cat',
            'description': 'Read a text file using a relative path.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'path': {'type': 'string'},
                },
                'required': ['path'],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'grep',
            'description': 'Search files for lines matching a regular expression.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'regex': {'type': 'string'},
                    'path': {'type': 'string'},
                },
                'required': ['regex', 'path'],
            },
        },
    },
]

load_dotenv()


def llm(messages, temperature=1, debug=False):
    """Send messages, handle tool requests, and return the final reply.

    >>> from unittest.mock import MagicMock, patch
    >>> call = MagicMock()
    >>> call.id = 'test-call-1'
    >>> call.function.name = 'calculate'
    >>> call.function.arguments = '{"expression": "2 + 3"}'
    >>> first = MagicMock()
    >>> first.choices[0].message.tool_calls = [call]
    >>> first.choices[0].message.model_dump.return_value = {
    ...     'role': 'assistant',
    ...     'tool_calls': [{
    ...         'id': 'test-call-1',
    ...         'type': 'function',
    ...         'function': {
    ...             'name': 'calculate',
    ...             'arguments': '{"expression": "2 + 3"}'
    ...         }
    ...     }]
    ... }
    >>> second = MagicMock()
    >>> second.choices[0].message.tool_calls = None
    >>> second.choices[0].message.content = 'The answer is 5.'
    >>> history = []
    >>> replies = [first, second]
    >>> def fake_create(messages, model, temperature, tools, timeout):
    ...     history.append(messages.copy())
    ...     return replies.pop(0)
    >>> with patch('chat.Groq') as mock_groq:
    ...     mock_groq.return_value.chat.completions.create.side_effect = fake_create
    ...     bot = Chat()
    ...     print(bot.send_message('What is 2 + 3?'))
    The answer is 5.
    >>> len(history)
    2
    >>> history[1][-1] == {
    ...     'role': 'tool',
    ...     'tool_call_id': 'test-call-1',
    ...     'content': '5'}
    True
    >>> history[1][-2]['role']
    'assistant'
    >>> bot.messages[-1]
    {'role': 'assistant', 'content': 'The answer is 5.'}
    """
    client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

    while True:
        completion = client.chat.completions.create(
            messages=messages,
            model='openai/gpt-oss-20b',
            temperature=temperature,
            tools=tools,
            timeout=30,
        )
        reply = completion.choices[0].message

        if not reply.tool_calls:
            return reply.content

        messages.append(reply.model_dump(exclude_none=True))

        for call in reply.tool_calls:
            name = call.function.name
            arguments = json.loads(call.function.arguments)
            if debug:
                print('Tool:', name, 'Arguments:', arguments)
            try:
                result = functions[name](**arguments)
            except (TypeError, KeyError) as error:
                result = 'Tool request error: ' + str(error)
            messages.append({
                'role': 'tool',
                'tool_call_id': call.id,
                'content': str(result),
            })


class Chat:
    """Keep conversation history and provide access to local tools.

    Each instance remembers its own messages and tool results.

    >>> bot = Chat(system='Be helpful.')
    >>> bot.messages
    [{'role': 'system', 'content': 'Be helpful.'}]
    >>> other = Chat()
    >>> bot.messages is other.messages
    False
    """
    def __init__(self, system='You are a helpful assistant.', debug=False):
        """Start a conversation with a system message and debug setting."""
        self.messages = [{'role': 'system', 'content': system}]
        self.debug = debug

    def send_message(self, message, temperature=0.8):
        """Send a message and remember the reply.

        >>> from unittest.mock import MagicMock, patch
        >>> response = MagicMock()
        >>> response.choices[0].message.content = 'Hello!'
        >>> response.choices[0].message.tool_calls = None
        >>> with patch('chat.Groq') as mock_groq:
        ...     mock_groq.return_value.chat.completions.create.return_value = response
        ...     bot = Chat()
        ...     bot.send_message('Hi', temperature=0)
        'Hello!'
        """
        self.messages.append({'role': 'user', 'content': message})
        reply = llm(self.messages, temperature=temperature, debug=self.debug)
        self.messages.append({'role': 'assistant', 'content': reply})
        return reply

    def run_command(self, command):
        """Run a manual tool command and remember its result.

        >>> bot = Chat()
        >>> bot.run_command('/calculate 2 + 3')
        '5'
        >>> bot.messages[-1]
        {'role': 'assistant', 'content': '5'}
        >>> bot.run_command('/cat ../secret.txt')
        'Error: unsafe path.'
        >>> bot.run_command('/unknown')
        'Error: unknown command or incorrect arguments.'
        >>> bot.run_command('/cat')
        'Error: unknown command or incorrect arguments.'
                >>> from unittest.mock import patch
        >>> bot = Chat()
        >>> with patch('chat.Groq', side_effect=AssertionError('API called')):
        ...     bot.run_command('/calculate 17 * 23')
        '391'
        >>> history = []
        >>> def fake_llm(messages, temperature, debug=False):
        ...     history.append(messages.copy())
        ...     return 'The result was 391.'
        >>> with patch('chat.llm', side_effect=fake_llm):
        ...     bot.send_message('What was the result?')
        'The result was 391.'
        >>> history[0][-3:] == [
        ...     {'role': 'user', 'content': '/calculate 17 * 23'},
        ...     {'role': 'assistant', 'content': '391'},
        ...     {'role': 'user', 'content': 'What was the result?'}]
        True
        """
        if command.strip() == '/compact':
            return compact(self)
        parts = shlex.split(command)
        name = parts[0]
        arguments = parts[1:]
        if self.debug:
            print('Command:', name, 'Arguments:', arguments)

        if name == '/ls' and len(arguments) == 0:
            result = ls()
        elif name == '/ls' and len(arguments) == 1:
            result = ls(arguments[0])
        elif name == '/cat' and len(arguments) == 1:
            result = cat(arguments[0])
        elif name == '/grep' and len(arguments) == 2:
            result = grep(arguments[0], arguments[1])
        elif name == '/calculate' and len(arguments) > 0:
            result = calculate(' '.join(arguments))
        else:
            result = 'Error: unknown command or incorrect arguments.'

        self.messages.append({'role': 'user', 'content': command})
        self.messages.append({'role': 'assistant', 'content': result})
        return result


def repl(temperature=0.8, debug=False):
    """Chat until EOFError or KeyboardInterrupt.

    >>> from unittest.mock import MagicMock, patch
    >>> response = MagicMock()
    >>> response.choices[0].message.content = 'Hello!'
    >>> response.choices[0].message.tool_calls = None
    >>> history = []
    >>> def fake_create(messages, model, temperature, tools, timeout):
    ...     history.append(messages.copy())
    ...     return response
    >>> with patch('builtins.input', side_effect=['Hi', 'Again', EOFError]):
    ...     with patch('chat.Groq') as mock_groq:
    ...         mock_groq.return_value.chat.completions.create.side_effect = fake_create
    ...         repl(temperature=0)
    Hello!
    Hello!
    <BLANKLINE>
    >>> history[1][1:] == [
    ...     {'role': 'user', 'content': 'Hi'},
    ...     {'role': 'assistant', 'content': 'Hello!'},
    ...     {'role': 'user', 'content': 'Again'}]
    True
    >>> with patch('builtins.input', side_effect=KeyboardInterrupt):
    ...     repl(temperature=0)
    <BLANKLINE>
    """

    chat = Chat(
        system='You are a helpful assistant. You always speak like a pirate.',
        debug=debug,
    )
    try:
        while True:
            user_input = input('chat> ')
            if user_input.startswith('/'):
                print(chat.run_command(user_input))
            else:
                print(chat.send_message(user_input, temperature=temperature))
    except (KeyboardInterrupt, EOFError):
        print()


def main(argv=None):
    """Run one message or start an interactive conversation.

    >>> from unittest.mock import patch
    >>> with patch('chat.llm', return_value='Hello!'):
    ...     main(['Hi'])
    Hello!
    >>> with patch('chat.repl') as mock_repl:
    ...     main([])
    >>> mock_repl.call_count
    1
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('message', nargs='?')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args(argv)

    if args.message is None:
        repl(debug=args.debug)
    else:
        bot = Chat(debug=args.debug)
        print(bot.send_message(args.message))


if __name__ == '__main__':
    main()
