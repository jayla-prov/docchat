"""Summarize a conversation into a shorter history."""


def compact(chat):
    r"""Replace conversation history with a summary of at most five lines.

    >>> from chat import Chat
    >>> from unittest.mock import patch
    >>> bot = Chat()
    >>> bot.messages.append({'role': 'user', 'content': 'I like cats.'})
    >>> original = bot.messages.copy()
    >>> requests = []
    >>> def fake_llm(messages, temperature):
    ...     requests.append(messages.copy())
    ...     return 'The user likes cats.'
    >>> with patch('chat.llm', side_effect=fake_llm):
    ...     compact(bot)
    'The user likes cats.'
    >>> requests[0][:-1] == original
    True
    >>> bot.messages
    [{'role': 'assistant', 'content': 'The user likes cats.'}]
    >>> with patch('chat.llm', return_value='1\n2\n3\n4\n5\n6'):
    ...     compact(bot)
    '1\n2\n3\n4\n5'
    >>> len(bot.messages)
    1
    """
    from chat import llm

    messages = chat.messages.copy()
    messages.append({
        'role': 'user',
        'content': (
            'Summarize this conversation in at most five lines. '
            'Preserve important facts, requests, and tool results. '
            'Return only the summary and do not call tools.'
        ),
    })
    summary = llm(messages, temperature=0)
    summary = '\n'.join(summary.split('\n')[:5])
    chat.messages = [{'role': 'assistant', 'content': summary}]
    return summary
