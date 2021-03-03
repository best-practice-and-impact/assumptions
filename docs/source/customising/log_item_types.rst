Log item types
==============

Log item types are classes that define items that you would like to capture in a log. They include:

1. the pattern used to capture your log items
2. the placeholder used in your templates to insert the log items
3. a parser to process a captured log item into the output text that is inserted into your template

To capture a custom log item you should define a new subclass of the ``LogItem`` base class.

``LogItem`` base class
----------------------

.. automodule:: assumptions.LogItem
    :members:

This base class is a subclass of the ``AbstractLogItem`` class, which defines the essential methods and parameters that a log item class require. This Abstract Base Class acts as an interface.

``AbstractLogItem`` interface
-----------------------------

.. automodule:: assumptions.log_items.AbstractLogItem
    :members:




The default log items captured by assumptions are assumptions and caveats.

``Assumption`` log item class
-----------------------------

.. automodule:: assumptions.log_items.Assumption
    :members:


``Caveat`` log item class
-----------------------------
.. automodule:: assumptions.log_items.Caveat
    :members:
