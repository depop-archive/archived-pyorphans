from __future__ import print_function
import sys

from .utils import find_orphan_dirs


def main(root_dir):
    """
    Main method for command-line execution. Prints details to stdout.

    Args:
        root_dir (str): path to root package of project to scan
            (must itself contain an __init__.py or be added to ignore file)
    """
    orphan_dir = None
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
            'If these are valid standalone python scripts, add them to .pyorphans_ignore file.'
        )


def entrypoint():
    """
    Entrypoint for command-line execution. Parses args.
    """
    main(sys.argv[1])
