Log templates
=============

Assumptions contains a few built-in Markdown templates for generating logs. Curly braces are used to indicate where log items and other dynamic content should be inserted into the template (e.g. ``{ assumptions }`` for assumptions). The representation of log items in the output log is defined in the corresponding log item class.


The date that the log is generated can be inserted into a template using the ``{ current_date }`` placeholder.

See the built-in templates below for example usage. Custom templates can be used with the command line interface using the ``-t`` flag and pointing to the template text file.

Assumptions and caveats log
---------------------------

The default template displays a list of assumptions and caveats. It also indicates the last time the template was updated.

.. literalinclude:: ../../../assumptions/templates/assumptions_caveats_log.md


Todo list
---------

This basic template creates a Markdown checklist from "Todo" comments in your code.

.. literalinclude:: ../../../assumptions/templates/todo_list.md
