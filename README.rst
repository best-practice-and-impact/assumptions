assumptions
===========

.. image:: https://badge.fury.io/py/assumptions.svg
    :target: https://pypi.org/project/assumptions/
    :alt: PyPI release

.. image:: https://github.com/foster999/assumptions/workflows/tests/badge.svg
    :target: https://github.com/foster999/assumptions/actions
    :alt: Actions build status

.. image:: https://readthedocs.org/projects/assumptions/badge/?version=latest
    :target: https://assumptions.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

See the `assumptions package documentation <https://assumptions.readthedocs.io>`_ for detailed usage and customisation.

Installation and Usage
----------------------

The Python package can be installed from PyPI:

.. code-block:: sh

    pip install assumptions


Run the command line tool to generate help documentation:

.. code-block:: sh

    assumptions -h

By default, assumptions will recursively search the current directory for assumptions and caveats, before writing the log to the same directory.

We recommend including assumptions in `pre-commit <https://pre-commit.com>`_ configurations:

.. code-block:: yaml

    repos:
    -   repo: https://github.com/foster999/assumptions
        rev: 1.1.0
        hooks:
        -   id: assumptions

This ensures that up-to-date logs are included in your project's version control.

Alternatively, the command line tool can be called as part of continuous integration workflows.
