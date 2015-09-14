Changelog
=========

0.4 (2015-09-14)
----------------

* direct wheel building support

* make all names available at the module level instead of requiring patching


0.3 (2015-07-03)
----------------

* removed patching of ``inspect.iscoroutine()`` as it is not ABC based


0.2 (2015-07-03)
----------------

* require explicit ``backports_abc.patch()`` call to do the patching
  (avoids side-effects on import and allows future configuration)

* provide access to patched names through global ``PATCHED`` dict

* add ABC based implementations of inspect.iscoroutine() and
  inspect.isawaitable()


0.1 (2015-06-24)
----------------

* initial public release

* provided ABCs: Generator, Coroutine, Awaitable
