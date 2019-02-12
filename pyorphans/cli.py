from __future__ import print_function
import sys

from .utils import find_orphan_dirs


CTRL_RED = '\033[91m'
CTRL_END = '\033[0m'


def main(*root_dirs):
    """
    Main method for command-line execution. Prints details to stdout.

    Args:
        *root_dirs (str): paths to root packages of project to scan
    """
    orphan_dir = None

    for root_dir in root_dirs:
        orphans_generator = find_orphan_dirs(root_dir)
        while True:
            try:
                orphan_dir, orphan_files = orphans_generator.next()
            except StopIteration:
                break

            print(orphan_dir)
            for orphan in orphan_files:
                print('-> %s' % orphan)
            if orphan_files:
                print('')

    if orphan_dir is None:
        # no orphans found!
        sys.exit(0)
    else:
        # orphans found
        sys.exit(
            CTRL_RED +
            'If these are valid standalone python scripts, add their '
            'parent dirs to the .pyorphans_ignore file.' +
            CTRL_END
        )


def entrypoint():
    """
    Entrypoint for command-line execution. Parses args.
    """
    main(*sys.argv[1:])
