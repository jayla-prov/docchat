import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

def llm(messages, temperature=1):
    completion = client.chat.completions.create(
        messages=messages,
        model='openai/gpt-oss-20b',
        temperature=temperature,
    )
    return completion.choices[0].message.content

class Chat:
    def __init__(self, system='You are a helpful assistant.'):
        self.messages = [{'role': 'system', 'content': system}]

    def send_message(self, message, temperature=0.8):
        """Send a message and remember the reply.

        >>> from unittest.mock import MagicMock, patch
        >>> response = MagicMock()
        >>> response.choices[0].message.content = 'Hello!'
        >>> with patch.object(client.chat.completions, 'create',
        ...                   return_value=response):
        ...     bot = Chat()
        ...     bot.send_message('Hi', temperature=0)
        'Hello!'
        """
        self.messages.append({'role': 'user', 'content': message})
        reply = llm(self.messages, temperature=temperature)
        self.messages.append({'role': 'assistant', 'content': reply})
        return reply


def repl(temperature=0.8):
    """Chat until EOFError or KeyboardInterrupt.

    >>> from unittest.mock import MagicMock, patch
    >>> response = MagicMock()
    >>> response.choices[0].message.content = 'Hello!'
    >>> history = []
    >>> def fake_create(messages, model, temperature):
    ...     history.append(messages.copy())
    ...     return response
    >>> with patch('builtins.input', side_effect=['Hi', 'Again', EOFError]):
    ...     with patch.object(client.chat.completions, 'create',
    ...                       side_effect=fake_create):
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
    chat = Chat(system='You are a helpful assistant. You always speak like a pirate.')
    try:
        while True:
            user_input = input('chat> ')
            print(chat.send_message(user_input, temperature=temperature))
    except (KeyboardInterrupt, EOFError):
        print()


if __name__ == '__main__':
    repl()