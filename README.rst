pyorphans
=========

|PyPI Version| |Build Status|

.. |PyPI Version| image:: http://img.shields.io/pypi/v/pyorphans.svg?style=flat
   :target: https://pypi.python.org/pypi/pyorphans/
   :alt: Latest PyPI version

.. |Build Status| image:: https://circleci.com/gh/depop/pyorphans.svg?style=shield&circle-token=772399d6adddb34029f8360892979c06b36c4df8
    :alt: Build Status

Find dirs which appear to be broken python packages, i.e. dirs which
contain ``*.py`` files without the necessary ``__init__.py``

Suggested use is to run as a `Pre-commit <https://pre-commit.com>`_ hook.


Why?
----

In your main code it's unlikely to have orphan modules since they are not importable and likely a cause of visible errors.

However in your unit tests, particularly if you have a lot of tests, you may find orphans. They go undetected because while developing you maybe pass the full path to the orphan to your test runner, and it works. But when you run the full suite of tests the orphans won't be found and so you have tests which aren't running!

By running ``pyorphans`` as a pre-commit hook you can catch the orphans and fix them immediately.


CLI Usage
---------

.. code:: bash

    pip install pyorphans

This will install a console script ``pyorphans``.

To run the checker, just pass it a list of the root packages in your project:

.. code:: bash

    pyorphans tests myproject

It returns output like:

.. code:: bash

	tests/unit
	-> test_important_stuff.py

	tests/integration/important_stuff
	tests/integration/important_stuff/api
	-> test_views.py

We can see here that ``tests/unit`` dir is missing an ``__init__.py`` but contains ``test_important_stuff.py``

Also ``tests/integration/important_stuff`` and ``tests/integration/important_stuff/api`` dirs are both missing their ``__init__.py`` files. Inside both directories is found a single 'orphan' file, ``tests/integration/important_stuff/api/test_views.py``.

Say you get an output like:

.. code:: bash

	myproject/scripts
	-> do_something.py

Maybe ``scripts`` is not intended to be a package and ``do_something.py`` is a perfectly good standalone script that runs from the command-line.

In this case create a ``.pyorphans_ignore`` file in the root of your project (the dir that pyorphans will be run from), containing:

.. code:: bash

	myproject/scripts

Now ``myproject/scripts`` (and all its subdirs) will be excluded from the search for orphans.


Pre-commit Hook
---------------

We suggest using `Pre-commit <https://pre-commit.com>`_.

.. code:: bash

	pip install pre-commit

Pyorphans is configured as a Pre-commit plugin. To apply it to your project, add a ``.pre-commit-config.yaml`` file to the root of your project like so:

.. code:: yaml

	repos:
	  - repo: https://github.com/depop/pyorphans
	    rev: "0.2.0"
	    hooks:
	    - id: pyorphans
	      args:
	        - myproject
	        - tests

Now every time you commit, Pyorphans will run and ask you to fix any that it finds. Pyorphans runs fast so you'll hardly notice it's there!
