import fnmatch
import os


IGNORE_FILE = '.pyorphans_ignore'


def dir_and_parents(dirname, root_dir):
    """
    Yields `dirname` and each of its parent dir paths, up to and including
    `root_dir`.

    Args:
        dirname (str): starting dir
        root_dir (str): dir to stop at

    Yields:
        str
    """
    yield dirname
    while dirname != root_dir:
        dirname = os.path.dirname(dirname)
        yield dirname


def get_ignore_dirs(ignore_file=IGNORE_FILE):
    """
    Some apparent orphans may be perfectly good standalone .py scripts which
    do not need to be part of a package.

    To ignore these files, add their immediate parent dir to a file named
    .pyorphans_ignore in root of the project.

    Yields dir paths to ignore.

    Args:
        ignore_file (str): path to a file containing dir paths to ignore

    Yields:
        str
    """
    try:
        with open(ignore_file) as f:
            for line in f.readlines():
                line = line.strip('\n').strip()
                if line:
                    yield line
    except IOError:
        # `ignore_file` not found
        pass


def find_orphan_dirs(root_dir, ignore_file=IGNORE_FILE):
    """
    Find dirs which appear to be broken python packages, i.e. dirs which
    contain .py files without the necessary __init__.py

    Args:
        root_dir (str): path to root package of project to scan
            (must itself contain an __init__.py or be added to ignore file)

    Yields:
        Tuple[str, List[str]]
            (<path to orphan dir>, [<orphaned .py path>, ...])
    """
    # dir paths to ignore (e.g. containing standalone .py scripts)
    ignore_dirs = {ignore_dir for ignore_dir in get_ignore_dirs(ignore_file)}

    # dir paths containing .py files (in any level of subdirs)
    pydirs = set()

    # dir paths containing an __init__.py file
    has_init_py = set()

    # associate .py files with directories
    potentially_orphaned = {}

    for current_dir, subdirs, filenames in os.walk(root_dir):
        pyfiles = fnmatch.filter(filenames, '*.py')
        if pyfiles:
            if '__init__.py' in pyfiles:
                has_init_py.add(current_dir)
            if current_dir in ignore_dirs:
                # don't recurse
                subdirs[:] = []
            else:
                pydirs.update(dir_and_parents(current_dir, root_dir))
                potentially_orphaned[current_dir] = pyfiles

    for pydir in sorted(pydirs):
        if any(
            parent not in has_init_py for parent in dir_and_parents(pydir, root_dir)
        ):
            yield pydir, sorted(potentially_orphaned.get(pydir, []))
