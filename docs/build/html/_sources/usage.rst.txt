User guide
==========

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

By default, the command line tool recursively searches the current directory for assumptions and caveats. These are summarised in an assumptions and caveats log, which is written to the current directory.

If the output log already exists, assumptions checks for any changes. If your documented assumptions and caveats haven't changed, assumptions doesn't overwrite the log to preserve the "last updated" date. Instead, it gives you a friendly nudge, just in case you've forgotten to update them.
