"""Search files for lines matching a regular expression."""

import glob
import re

from tools.path_utils import is_path_safe


def grep(regex, path):
    r"""Return matching lines from files selected by a safe path pattern.

    >>> grep('hello', '/etc/passwd')
    'Error: unsafe path.'
    >>> grep('hello', '../*.txt')
    'Error: unsafe path.'
    >>> import os
    >>> from tempfile import TemporaryDirectory
    >>> with TemporaryDirectory(dir='.') as folder:
    ...     folder = os.path.relpath(folder)
    ...     with open(folder + '/a.txt', 'w', encoding='utf-8') as f:
    ...         written = f.write('TODO homework\nFinished\nTODO homework\n')
    ...     with open(folder + '/b.txt', 'w', encoding='utf-8') as f:
    ...         written = f.write('TODO study\n')
    ...     result = grep('TODO', folder + '/*.txt')
    ...     print(result == 'TODO homework\nTODO homework\nTODO study\n')
    ...     print(grep('^Finished', folder + '/*.txt') == 'Finished\n')
    ...     print(grep('nothing', folder + '/*.txt') == '')
    ...     print(grep('TODO', folder + '/missing.txt') == '')
    ...     with open(folder + '/bad.txt', 'wb') as f:
    ...         written = f.write(b'\xff')
    ...     print(grep('TODO', folder + '/bad.txt'))
    True
    True
    True
    True
    Error: could not read file.
    """
    if not is_path_safe(path):
        return 'Error: unsafe path.'

    matches = []
    for filename in sorted(glob.glob(path)):
        try:
            with open(filename, encoding='utf-8') as f:
                for line in f:
                    if re.search(regex, line):
                        matches.append(line)
        except (OSError, UnicodeDecodeError):
            return 'Error: could not read file.'

    return ''.join(matches)
