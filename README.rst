pyorphans
======

|PyPI Version| |Build Status|

.. |PyPI Version| image:: http://img.shields.io/pypi/v/pyorphans.svg?style=flat
   :target: https://pypi.python.org/pypi/pyorphans/
   :alt: Latest PyPI version

.. |Build Status| image:: https://circleci.com/gh/depop/pyorphans.svg?style=shield&circle-token=772399d6adddb34029f8360892979c06b36c4df8
    :alt: Build Status

Find dirs which appear to be broken python packages, i.e. dirs which
contain ``*.py`` files without the necessary ``__init__.py``

Suggested use is to run as a `Pre-commit <https://pre-commit.com>`_ hook.

Usage
-----

.. code:: bash

    pip install pyorphans

