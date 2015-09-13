=============
ABC-Backports
=============

Usage:

.. code-block:: python

    import backports_abc
    backports_abc.patch()

    try:
        # ABCs live in "collections.abc" in Python >= 3.3
        from collections.abc import Coroutine, Generator
    except ImportError:
        # fall back to import from "collections" in Python <= 3.2
        from collections import Coroutine, Generator

Currently provides the following names if missing:

* ``collections.abc.Generator``
* ``collections.abc.Awaitable``
* ``collections.abc.Coroutine``
* ``inspect.isawaitable(obj)``

In Python 2.x and Python 3.2, it patches the ``collections`` module
instead of the ``collections.abc`` module.  Any names that are already
available when calling ``patch()`` will not be overwritten.

The names that were previously patched by ``patch()`` can be queried
through the mapping in ``backports_abc.PATCHED``.
