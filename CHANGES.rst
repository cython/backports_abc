Changelog
=========

0.3
---

* removed patching of ``inspect.iscoroutine()`` as it is not ABC based


0.2
---

* require explicit ``backports_abc.patch()`` call to do the patching
  (avoids side-effects on import and allows future configuration)

* provide access to patched names through global ``PATCHED`` dict

* add ABC based implementations of inspect.iscoroutine() and
  inspect.isawaitable()


0.1
---

* initial public release

* provided ABCs: Generator, Coroutine, Awaitable
