Log templates
=============

Assumptions contains a few built-in Markdown templates for generating logs. Curly braces are used to indicate where log items and other dynamic content should be inserted into the template (e.g. ``{ assumptions }`` for assumptions).

Assumptions and caveats log
---------------------------

The default template displays a list of assumptions and caveats. It also indicates the last time the template was updated.

.. literalinclude:: ../../../assumptions/templates/assumptions_caveats_log.md


Todo list
---------

This basic template creates a Markdown checklist from "Todo" comments in your code.

.. literalinclude:: ../../../assumptions/templates/todo_list.md
