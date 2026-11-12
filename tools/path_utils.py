"""Check paths before using file tools."""


def is_path_safe(path):
    """Return whether a path is relative and has no parent-directory parts.

    >>> is_path_safe('notes.txt')
    True
    >>> is_path_safe('documents/notes.txt')
    True
    >>> is_path_safe('.')
    True
    >>> is_path_safe('/etc/passwd')
    False
    >>> is_path_safe('../notes.txt')
    False
    >>> is_path_safe('documents/../notes.txt')
    False
    """
    if path.startswith('/'):
        return False
    if '..' in path.split('/'):
        return False
    return True
