"""Demonstrate a tool request without contacting a model."""
import json


def word_count(text):
    """Count words separated by whitespace.

    >>> word_count('game night starts soon')
    4
    """
    return len(text.split())


functions = {'word_count': word_count}
tools = [{
    'type': 'function',
    'function': {
        'name': 'word_count',
        'description': 'Count words separated by whitespace.',
        'parameters': {
            'type': 'object',
            'properties': {'text': {'type': 'string'}},
            'required': ['text'],
        },
    },
}]
messages = [{'role': 'user', 'content': 'Count the words in game night starts soon.'}]

# Stand in for the model's first reply, which requests a Python function.
request = {
    'role': 'assistant',
    'content': None,
    'tool_calls': [{
        'id': 'example-call-1',
        'type': 'function',
        'function': {
            'name': 'word_count',
            'arguments': '{"text": "game night starts soon"}',
        },
    }],
}
messages.append(request)
for call in request['tool_calls']:
    name = call['function']['name']
    arguments = json.loads(call['function']['arguments'])
    result = functions[name](**arguments)
    messages.append({
        'role': 'tool',
        'tool_call_id': call['id'],
        'content': str(result),
    })
print(messages[-1])