import pytest

from pyorphans.cli import CTRL_END, CTRL_RED, main


def test_main(capsys):
    with pytest.raises(SystemExit) as exc:
        main('testdir')

    assert exc.value.code == (
        CTRL_RED +
        'If these are valid standalone python scripts, add their '
        'parent dirs to the .pyorphans_ignore file.' +
        CTRL_END
    )
    captured = capsys.readouterr()
    assert captured.out == (
        'testdir/broken_package1\n'
        'testdir/broken_package1/broken_package2\n'
        '-> __init__.py\n'
        '-> orphan1.py\n'
        '\n'
        'testdir/good_package1/non_package1\n'
        '-> ignore_me1.py\n'
        '\n'
        'testdir/good_package1/non_package1/broken_package4\n'
        '-> also_ignored1.py\n'
        '\n'
        'testdir/good_package4/broken_package3\n'
        '-> orphan2.py\n'
        '\n'
        'testdir/good_package4/non_package3\n'
        '-> ignore_me2.py\n'
        '\n'
    )
    assert captured.err == ''
