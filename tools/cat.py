"""read text files using a checked relative path."""

from tools.path_utils import is_path_safe


def cat(path):
    r"""Return a text file's contents, or an error message.

    >>> cat('/etc/passwd')
    'Error: unsafe path.'
    >>> cat('../notes.txt')
    'Error: unsafe path.'
    >>> import os
    >>> from tempfile import TemporaryDirectory
    >>> with TemporaryDirectory(dir='.') as folder:
    ...     folder = os.path.relpath(folder)
    ...     filename = folder + '/notes.txt'
    ...     with open(filename, 'w', encoding='utf-8') as f:
    ...         written = f.write('Hello!\nSecond line.')
    ...     print(cat(filename))
    ...     print(cat(folder + '/missing.txt'))
    ...     with open(filename, 'wb') as f:
    ...         written = f.write(b'\xff')
    ...     print(cat(filename))
    Hello!
    Second line.
    Error: could not read file.
    Error: could not read file.
    """
    if not is_path_safe(path):
        return 'Error: unsafe path.'

    try:
        with open(path, encoding='utf-8') as f:
            return f.read()
    except (OSError, UnicodeDecodeError):
        return 'Error: could not read file.'
