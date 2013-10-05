===============
XAIL for Python
===============

XAIL is a new standard for conversational robots, interactive help, and like.
It currently has three main engines: regex, matrix [1]_, and substring.
There is also a generic response engine.

If you are looking for a featured chatterot, you should look for the ``HAL``
package instead, which implements a chatterbot in top of this library.

This library contains only basic matching. You may have to define your own
post-processing for more advanced features.

.. [1] matches if all the keyword exists in the input, after stemming

Installation
============

To install, do: ``pip install XAIL``.

After installation, run python in interactive mode and run
``import xail.dbtest``. If it says you don't have full-text search, then you
should install the ``pysqlite2`` module from `here
<http://code.google.com/p/pysqlite/downloads/list>`_. If you don't, PyXAIL
will still function, albeit slower, and may lower the quality of responses.
