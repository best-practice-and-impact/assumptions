User guide
==========

Installation and usage
----------------------

The assumptions package can be installed from PyPI:

.. code-block:: sh

    pip install assumptions

Run the command line tool to generate help documentation:

.. code-block:: sh

    assumptions -h


.. jupyter-execute::
    :hide-code:

    import subprocess

    print(
        subprocess.run(["assumptions", "-h"], stdout=subprocess.PIPE).stdout.decode("utf-8")
    )

We recommend including assumptions in `pre-commit <https://pre-commit.com>`_ configurations:

.. code-block:: yaml

    repos:
    -   repo: https://github.com/foster999/assumptions
        rev: 1.1.0
        hooks:
        -   id: assumptions

This ensures that up-to-date logs are included in your project's version control.

Alternatively, the command line tool can be called as part of continuous integration workflows.

Assumptions and caveats
-----------------------

By default, assumptions will recursively search the current directory for assumptions and caveats, before writing the log to the same directory.

Assumptions and caveats should be written in you code as hashed comments:

.. code-block:: py

    # Assumption: Title of assumption
    # Quality: RED
    # Impact: AMBER
    # Detailed description
    # on next line or many.

.. code-block:: py

    # Caveat: Oh oh
    # Something isn't quite what it seems


Or using the R {roxygen} `@section` tag:

.. code-block:: R

    #' Square a number
    #'
    #' @param x the input to be squared
    #' @section Assumption: Numbers are used
    #' No strings please.
    square <- function(x){
      return(x^2)
    }

.. code-block:: R

    #' Square a number
    #'
    #' @param x the input to be squared
    #' @section Caveat: Only tested with real numbers
    square <- function(x){
      return(x^2)
    }


By default, the assumptions command line tool recursively searches the current directory for assumptions and caveats. These are summarised in an assumptions and caveats log, which is written to the current directory.

.. code-block:: sh

    assumptions

.. jupyter-execute::
    :hide-code:

    import subprocess

    print(
        subprocess.run(
            ["assumptions", "-e", ".py", "--dry-run"], stdout=subprocess.PIPE
        ).stdout.decode("utf-8")
    )

If the output log already exists, assumptions checks for any changes. If your documented assumptions and caveats haven't changed, assumptions doesn't overwrite the log to preserve the "last updated" date. Instead, it gives you a friendly nudge, just in case you've forgotten to update them.
