assumptions
===========

Acknowledging the assumptions and caveats in our analysis is an essential part of quality assurance.
When the code changes, this should be reflected in our documentation.

Record your analytical assumptions and caveats in code comments:

.. code-block:: py

    # Assumption: Title of assumption
    # Quality: RED
    # Impact: AMBER
    # Detailed description
    # on one line or many.


Assumptions will generate a Markdown assumptions logs for your documentation:

.. code-block:: markdown

    ### Assumption 1: Title of assumption

    * Location: `test_git_assumptions/search_here/assumptions.py`
    * **Quality**: RED
    * **Impact**: AMBER

    Detailed description on one line or many.

By the way, :ref:`assumptions can also be customised<customising>` to find any text pattern and insert matches into any template text document.

.. toctree::
   :caption: Documentation
   :maxdepth: 2

   usage.rst
   example/index.rst
   customising/index.rst
