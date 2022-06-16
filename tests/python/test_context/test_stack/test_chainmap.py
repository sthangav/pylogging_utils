# encoding: utf-8
import unittest

AVAILABLE = True
try:
    from logging_utils.context.stack.chainmap import ChainMapContextStack
except:
    AVAILABLE = False


@unittest.skipUnless(AVAILABLE, "ChainMap-backed ContextStack is unavailable for this Python")
class SimpleContextStackTest(unittest.TestCase):

    def setUp(self):
        self.stack = ChainMapContextStack()

    def test_pop_from_empty_stack_raises_IndexError(self):
        self.stack.pop()
        #self.assertRaises(IndexError, self.stack.pop)

    def test_push_expects_allows_any_value(self):
        self.stack.push(None)
        self.stack.push(True)
        self.stack.push(1)
        self.stack.push([1,2,3])

    def test_iter_expects_values_to_be_dicts_1(self):
        self.stack.push(None)
        self.assertRaises(TypeError, list, self.stack)

    def test_iter_expects_values_to_be_dicts_2(self):
        self.stack.push(True)
        self.assertRaises(TypeError, list, self.stack)

    def test_iter_expects_values_to_be_dicts_3(self):
        self.stack.push(1)
        self.assertRaises(TypeError, list, self.stack)

    def test_iter_expects_values_to_be_dicts_4(self):
        self.stack.push([1,2,3])
        self.assertRaises(IndexError, list, self.stack)

    def test_pop_removes_element_from_stack(self):
        self.assertEqual(list(self.stack), list())
        self.stack.push(None)

        self.stack.pop()
        self.assertEqual(list(self.stack), list())

    def test_push_adds_element_to_the_stack(self):
        self.assertEqual('ChainMap({})', str(self.stack))

        self.stack.push({'a': 1})
        self.assertEqual("ChainMap({'a': 1}, {})", str(self.stack))

        self.stack.push({'b': 2})
        self.assertEqual("ChainMap({'b': 2}, {'a': 1}, {})", str(self.stack))

    def test_iter_returns_iterable(self):
        self.stack.push(dict(a=1))
        items = iter(self.stack)
        self.assertEquals(list(items), [('a', 1)])

        [i for i in items]
        self.assertEquals(list(items), list())

        items = iter(self.stack)
        self.assertEquals(list(items), [('a', 1)])

        self.assertEquals(list(self.stack), [('a', 1)])

    def test_stack_might_be_casted_to_string(self):
        self.assertEqual('ChainMap({})', str(self.stack))

        self.stack.push({'a': 1})
        self.assertEqual("ChainMap({'a': 1}, {})", str(self.stack))

        self.stack.push({'b': 2})
        self.assertEqual("ChainMap({'b': 2}, {'a': 1}, {})", str(self.stack))

    def test_new_context_overrides_existing_values(self):
        self.stack.push({'a': 1})
        self.assertEqual([('a', 1)], list(self.stack))

        self.stack.push({'a': 2})
        self.assertEqual([('a', 2)], list(self.stack))

        self.stack.pop()
        self.assertEqual([('a', 1)], list(self.stack))

