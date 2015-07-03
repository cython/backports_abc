=============
ABC-Backports
=============

Usage::

    import backports_abc
    backports_abc.patch()

    try:
        from collections.abc import Coroutine, Generator
    except ImportError:
        from collections import Coroutine, Generator

Currently provides the following names if missing:

* ``collections.abc.Generator``
* ``collections.abc.Awaitable``
* ``collections.abc.Coroutine``
* ``inspect.isawaitable(obj)``

In Python 2.x, it patches the ``collections`` module instead of the
``collections.abc`` module

The names that were previously patched by ``patch()`` can be queried
through the mapping in ``backports_abc.PATCHED``.
