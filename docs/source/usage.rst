User guide
==========

Installation and usage
----------------------

The assumptions package can currently be installed from GitHub:

.. code-block:: sh

    pip install git+https://github.com/foster999/assumptions.git

Run the command line tool to generate help documentation:

.. code-block:: sh

    assumptions -h


.. jupyter-execute::
    :hide-code:

    import subprocess

    print(subprocess.run(["assumptions", "-h"], capture_output=True).stdout.decode())


Assumptions and caveats log
---------------------------

Assumptions and caveats should be written in you code as comments in the following format:

.. code-block:: py

    # Assumption: Title of assumption
    # Quality: RED
    # Impact: AMBER
    # Detailed description
    # on next line or many.

.. code-block:: py

    # Caveat: Oh oh
    # Something isn't quite what it seems


By default, the assumptions command line tool recursively searches the current directory for assumptions and caveats. These are summarised in an assumptions and caveats log, which is written to the current directory.

.. code-block:: sh

    assumptions

.. jupyter-execute::
    :hide-code:

    import subprocess

    print(subprocess.run(["assumptions"], capture_output=True).stdout.decode())

If the output log already exists, assumptions checks for any changes. If your documented assumptions and caveats haven't changed, assumptions doesn't overwrite the log to preserve the "last updated" date. Instead, it gives you a friendly nudge, just in case you've forgotten to update them.
