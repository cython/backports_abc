"""
Test suite originally copied from test_collections.py in Python 3.5.
"""

import backports_abc

FROM_MODULE = [
    backports_abc.Generator,
    backports_abc.Coroutine,
    backports_abc.Awaitable,
    backports_abc.isawaitable,
]

backports_abc.patch()

try:
    from collections.abc import (
        Generator, Coroutine, Awaitable, Iterator, Iterable)
except ImportError:
    from collections import (
        Generator, Coroutine, Awaitable, Iterator, Iterable)

import sys
import inspect
import unittest
import operator
from gc import collect as gc_collect


IS_PY3 = sys.version_info[0] >= 3


class BackportsAbcTest(unittest.TestCase):

    def validate_module_namespace(self):
        self.assertEqual(FROM_MODULE[0], Generator)
        self.assertEqual(FROM_MODULE[1], Coroutine)
        self.assertEqual(FROM_MODULE[2], Awaitable)
        self.assertEqual(FROM_MODULE[3], inspect.isawaitable)


################################################################################
### Abstract Base Classes
################################################################################

class ABCTestCase(unittest.TestCase):

    def validate_abstract_methods(self, abc, *names):
        methodstubs = dict.fromkeys(names, lambda s, *args: 0)

        # everything should work will all required methods are present
        C = type('C', (abc,), methodstubs)
        C()

        # instantiation should fail if a required method is missing
        for name in names:
            stubs = methodstubs.copy()
            del stubs[name]
            C = type('C', (abc,), stubs)
            self.assertRaises(TypeError, C, name)

    def validate_isinstance(self, abc, name):
        stub = lambda s, *args: 0

        C = type('C', (object,), {'__hash__': None})
        setattr(C, name, stub)
        self.assertIsInstance(C(), abc)
        self.assertTrue(issubclass(C, abc))

        C = type('C', (object,), {'__hash__': None})
        self.assertNotIsInstance(C(), abc)
        self.assertFalse(issubclass(C, abc))

    def validate_comparison(self, instance):
        ops = ['lt', 'gt', 'le', 'ge', 'ne', 'or', 'and', 'xor', 'sub']
        operators = {}
        for op in ops:
            name = '__' + op + '__'
            operators[name] = getattr(operator, name)

        class Other(object):
            def __init__(self):
                self.right_side = False
            def __eq__(self, other):
                self.right_side = True
                return True
            __lt__ = __eq__
            __gt__ = __eq__
            __le__ = __eq__
            __ge__ = __eq__
            __ne__ = __eq__
            __ror__ = __eq__
            __rand__ = __eq__
            __rxor__ = __eq__
            __rsub__ = __eq__

        for name, op in operators.items():
            if not hasattr(instance, name):
                continue
            other = Other()
            op(instance, other)
            self.assertTrue(other.right_side,'Right side not called for %s.%s'
                            % (type(instance), name))

    if not hasattr(unittest.TestCase, 'assertRaisesRegex'):
        def assertRaisesRegex(self, exc, regex, func, *args, **kwargs):
            try:
                func(*args, **kwargs)
            except exc:
                self.assertTrue(True)
            else:
                self.assertFalse(True)

    if not hasattr(unittest.TestCase, 'assertIs'):
        def assertIs(self, obj, t):
            self.assertTrue(obj is t, repr(obj))

    if not hasattr(unittest.TestCase, 'assertIsNone'):
        def assertIsNone(self, obj):
            self.assertTrue(obj is None, repr(obj))

    if not hasattr(unittest.TestCase, 'assertIsInstance'):
        def assertIsInstance(self, obj, t):
            self.assertTrue(isinstance(obj, t), repr(obj))

    if not hasattr(unittest.TestCase, 'assertNotIsInstance'):
        def assertNotIsInstance(self, obj, t):
            self.assertFalse(isinstance(obj, t), repr(obj))


class TestOneTrickPonyABCs(ABCTestCase):

    def test_Awaitable(self):
        def gen():
            yield

        #@types.coroutine
        #def coro():
        #    yield

        #async def new_coro():
        #    pass

        class Bar(object):
            def __await__(self):
                yield

        class MinimalCoro(Coroutine):
            def send(self, value):
                return value
            def throw(self, typ, val=None, tb=None):
                super(MinimalCoro, self).throw(typ, val, tb)
            def __await__(self):
                yield

        non_samples = [None, int(), gen(), object()]
        for x in non_samples:
            self.assertNotIsInstance(x, Awaitable)
            self.assertFalse(issubclass(type(x), Awaitable), repr(type(x)))
            self.assertFalse(inspect.isawaitable(x))

        samples = [Bar(), MinimalCoro()]
        for x in samples:
            self.assertIsInstance(x, Awaitable)
            self.assertTrue(issubclass(type(x), Awaitable))
            self.assertTrue(inspect.isawaitable(x))

        #c = coro()
        #self.assertIsInstance(c, Awaitable)
        #c.close() # awoid RuntimeWarning that coro() was not awaited

        #c = new_coro()
        #self.assertIsInstance(c, Awaitable)
        #c.close() # awoid RuntimeWarning that coro() was not awaited

        class CoroLike(object): pass
        Coroutine.register(CoroLike)
        self.assertTrue(inspect.isawaitable(CoroLike()))
        self.assertTrue(isinstance(CoroLike(), Awaitable))
        self.assertTrue(issubclass(CoroLike, Awaitable))
        CoroLike = None
        gc_collect() # Kill CoroLike to clean-up ABCMeta cache

    def test_Coroutine(self):
        def gen():
            yield

        #@types.coroutine
        #def coro():
        #    yield

        #async def new_coro():
        #    pass

        class Bar(object):
            def __await__(self):
                yield

        class MinimalCoro(Coroutine):
            def send(self, value):
                return value
            def throw(self, typ, val=None, tb=None):
                super(MinimalCoro, self).throw(typ, val, tb)
            def __await__(self):
                yield

        non_samples = [None, int(), gen(), object(), Bar()]
        for x in non_samples:
            self.assertNotIsInstance(x, Coroutine)
            self.assertFalse(issubclass(type(x), Coroutine), repr(type(x)))

        samples = [MinimalCoro()]
        for x in samples:
            self.assertIsInstance(x, Awaitable)
            self.assertTrue(issubclass(type(x), Awaitable))

        #c = coro()
        #self.assertIsInstance(c, Coroutine)
        #c.close() # awoid RuntimeWarning that coro() was not awaited

        #c = new_coro()
        #self.assertIsInstance(c, Coroutine)
        #c.close() # awoid RuntimeWarning that coro() was not awaited

        class CoroLike(object):
            def send(self, value):
                pass
            def throw(self, typ, val=None, tb=None):
                pass
            def close(self):
                pass
            def __await__(self):
                pass
        self.assertTrue(isinstance(CoroLike(), Coroutine))
        self.assertTrue(issubclass(CoroLike, Coroutine))

        class CoroLike(object):
            def send(self, value):
                pass
            def close(self):
                pass
            def __await__(self):
                pass
        self.assertFalse(isinstance(CoroLike(), Coroutine))
        self.assertFalse(issubclass(CoroLike, Coroutine))

    def test_Iterable(self):
        # Check some non-iterables
        class OldStyleNonIterable: pass
        non_samples = [None, 42, 3.14, 1j, OldStyleNonIterable()]
        for x in non_samples:
            self.assertNotIsInstance(x, Iterable)
            self.assertFalse(issubclass(x.__class__, Iterable),
                             repr(x.__class__))
        # Check some iterables
        class OldStyleIterableBase:
            def __iter__(self):
                yield None
        class OldStyleIterable(OldStyleIterableBase): pass
        samples = [bytes(), str(),
                   tuple(), list(), set(), frozenset(), dict(),
                   dict().keys(), dict().items(), dict().values(),
                   (lambda: (yield))(),
                   (x for x in []),
                   OldStyleIterable(),
                   ]
        for x in samples:
            self.assertIsInstance(x, Iterable)
            self.assertTrue(issubclass(x.__class__, Iterable),
                            repr(x.__class__))
        # Check direct subclassing
        class I(Iterable):
            def __iter__(self):
                return super(I, self).__iter__()
        self.assertEqual(list(I()), [])
        self.assertFalse(issubclass(str, I))
        self.validate_abstract_methods(Iterable, '__iter__')
        self.validate_isinstance(Iterable, '__iter__')

    def test_Iterator(self):
        non_samples = [None, 42, 3.14, 1j, b"", "", (), [], {}, set()]
        for x in non_samples:
            self.assertNotIsInstance(x, Iterator)
            self.assertFalse(issubclass(type(x), Iterator), repr(type(x)))
        samples = [iter(bytes()), iter(str()),
                   iter(tuple()), iter(list()), iter(dict()),
                   iter(set()), iter(frozenset()),
                   iter(dict().keys()), iter(dict().items()),
                   iter(dict().values()),
                   (lambda: (yield))(),
                   (x for x in []),
                   ]
        for x in samples:
            self.assertIsInstance(x, Iterator)
            self.assertTrue(issubclass(type(x), Iterator), repr(type(x)))
        self.validate_abstract_methods(Iterator, '__next__' if IS_PY3 else 'next', '__iter__')

        # Issue 10565
        class NextOnly(object):
            def __next__(self):
                yield 1
                return
        self.assertNotIsInstance(NextOnly(), Iterator)

    def test_Generator(self):
        class NonGen1(object):
            def __iter__(self): return self
            def __next__(self): return None
            def close(self): pass
            def throw(self, typ, val=None, tb=None): pass

        class NonGen2(object):
            def __iter__(self): return self
            def __next__(self): return None
            def close(self): pass
            def send(self, value): return value

        class NonGen3(object):
            def close(self): pass
            def send(self, value): return value
            def throw(self, typ, val=None, tb=None): pass

        non_samples = [
            None, 42, 3.14, 1j, b"", "", (), [], {}, set(),
            iter(()), iter([]), NonGen1(), NonGen2(), NonGen3()]
        for x in non_samples:
            self.assertNotIsInstance(x, Generator)
            self.assertFalse(issubclass(type(x), Generator), repr(type(x)))

        class Gen(object):
            def __iter__(self): return self
            if IS_PY3:
                def __next__(self): return None
            else:
                def next(self): return None
            def close(self): pass
            def send(self, value): return value
            def throw(self, typ, val=None, tb=None): pass

        class MinimalGen(Generator):
            def send(self, value):
                return value
            def throw(self, typ, val=None, tb=None):
                super(MinimalGen, self).throw(typ, val, tb)

        def gen():
            yield 1

        samples = [gen(), (lambda: (yield))(), Gen(), MinimalGen()]
        for x in samples:
            self.assertIsInstance(x, Iterator)
            self.assertIsInstance(x, Generator)
            self.assertTrue(issubclass(type(x), Generator), repr(type(x)))
        self.validate_abstract_methods(Generator, 'send', 'throw')

        # mixin tests
        mgen = MinimalGen()
        self.assertIs(mgen, iter(mgen))
        self.assertIs(mgen.send(None), next(mgen))
        self.assertEqual(2, mgen.send(2))
        self.assertIsNone(mgen.close())
        self.assertRaises(ValueError, mgen.throw, ValueError)
        self.assertRaisesRegex(ValueError, "^huhu$",
                               mgen.throw, ValueError, ValueError("huhu"))
        self.assertRaises(StopIteration, mgen.throw, StopIteration())

        class FailOnClose(Generator):
            def send(self, value): return value
            def throw(self, *args): raise ValueError

        self.assertRaises(ValueError, FailOnClose().close)

        class IgnoreGeneratorExit(Generator):
            def send(self, value): return value
            def throw(self, *args): pass

        self.assertRaises(RuntimeError, IgnoreGeneratorExit().close)


if __name__ == '__main__':
    unittest.main()
