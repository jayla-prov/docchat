"""Evaluates arithmetic expressions after checking their characters."""


def calculate(expression):
    """Return an arithmetic result as text, or an error message.

    >>> calculate('2 + 3 * 4')
    '14'
    >>> calculate('(10 - 4) / 2')
    '3.0'
    >>> calculate('abs(-3)')
    'Error: invalid character.'
    >>> calculate('hello')
    'Error: invalid character.'
    >>> calculate('2 +')
    'Error: invalid expression.'
    >>> calculate('1 / 0')
    'Error: invalid expression.'
    >>> calculate('')
    'Error: invalid expression.'
    """
    allowed = '0123456789 +-*/%.()'
    for character in expression:
        if character not in allowed:
            return 'Error: invalid character.'

    try:
        return str(eval(expression))
    except (SyntaxError, ZeroDivisionError, TypeError, ValueError, OverflowError):
        return 'Error: invalid expression.'
