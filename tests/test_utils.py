import pytest

from pyorphans.utils import (
    dir_and_parents,
    get_ignore_dirs,
    find_orphan_dirs,
)


@pytest.mark.parametrize("dirname,root_dir,expected", [
    ("testdir", "testdir", ["testdir"]),
    ("testdir/good_package1/good_package2", "testdir", [
        "testdir/good_package1/good_package2",
        "testdir/good_package1",
        "testdir"]),
])
def test_dir_and_parents(dirname, root_dir, expected):
    result = [_ for _ in dir_and_parents(dirname, root_dir)]
    assert result == expected


def test_get_ignore_dirs():
    result = [_ for _ in get_ignore_dirs("tests/ignorefile")]
    assert result == [
        "testdir/good_package1/non_package1",
        "testdir/good_package4/non_package3",
    ]


def test_find_orphan_dirs():
    result = [_ for _ in find_orphan_dirs("testdir", ignore_file="tests/ignorefile")]
    assert result == [
        ('testdir/broken_package1', []),
        ('testdir/broken_package1/broken_package2', ['__init__.py', 'orphan1.py']),
        ('testdir/good_package4/broken_package3', ['orphan2.py']),
    ]
