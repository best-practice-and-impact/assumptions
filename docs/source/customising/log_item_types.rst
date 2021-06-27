Log item types
==============

Log item types are classes that define items that you would like to capture in a log. These classes store:

* a list of regular expression patterns used to capture your log items,
* the placeholder used in your templates to insert the log items,
* the text displayed in the template if no log items are found,
* and a parser method to process a captured log item into the output text that is inserted into your template.

To capture a custom log item you can define a new subclass of the ``LogItem`` base class:

``LogItem`` base class
----------------------

.. automodule:: assumptions.LogItem
    :members:


Example log item types
----------------------

The default log items captured by ``assumptions`` are assumptions, caveats and todos. Their class definitions provide examples that implement the abstract properties and methods described above. You can use these as a good starting point when defining your own log item type:

.. literalinclude:: ../../../assumptions/log_items.py
   :language: py
   :lines: 120-
