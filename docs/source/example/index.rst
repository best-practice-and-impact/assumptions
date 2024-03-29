Example output logs
===================

This sections demonstrates what output logs look like when included in documentation generated by `sphinx`.

.. toctree::
    :caption: Examples
    :maxdepth: 1
    :hidden:

    assumptions_caveats_log.md
    technical_debt_log.md
    todo_list.md

Assumptions and caveats log
---------------------------

The `example assumtions and caveats log <assumptions_caveats_log.html>`_ is generated from the root of this project using:

.. code-block:: sh

    assumptions -e .py -o docs/source/example/assumptions_caveats_log.md

Technical debt log
------------------

The `example technical debt log <technical_debt_log.html>`_ is generated from the root of this project using:

.. code-block:: sh

    assumptions -e .py -o docs/source/example/technical_debt_log.md -l technical_debt_log

Todo list
---------

The `example todo list <todo_list.html>`_ is generated from the root of this project using:

.. code-block:: sh

    assumptions -e .py -o docs/source/example/todo_list.md -l todo_list
