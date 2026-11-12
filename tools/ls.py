"""List folder contents in sorted order."""

import glob

from tools.path_utils import is_path_safe


def ls(path='.'):
    """Return sorted names from a folder, or an error message.

    >>> ls('/etc')
    'Error: unsafe path.'
    >>> ls('../')
    'Error: unsafe path.'
    >>> import os
    >>> from tempfile import TemporaryDirectory
    >>> with TemporaryDirectory(dir='.') as folder:
    ...     folder = os.path.relpath(folder)
    ...     print(ls(folder) == '')
    ...     for name in ['zebra.txt', 'apple.txt']:
    ...         with open(folder + '/' + name, 'w') as f:
    ...             written = f.write('example')
    ...     print(ls(folder))
    True
    apple.txt
    zebra.txt
    """
    if not is_path_safe(path):
        return 'Error: unsafe path.'

    files = glob.glob(path + '/*')
    names = [filename.split('/')[-1] for filename in files]
    return '\n'.join(sorted(names))
