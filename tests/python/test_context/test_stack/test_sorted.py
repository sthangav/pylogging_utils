# encoding: utf-8
import unittest

from logging_utils._compat import mock
from logging_utils.context.stack.sorted import SortedContextStack


class SimpleContextStackTest(unittest.TestCase):

    def setUp(self):
        self.inner = mock.MagicMock(spec=SortedContextStack)
        self.inner.__str__.return_value = "foo"
        self.inner.__iter__.return_value = [("b", 1), ("a", 2), ("a", 1)]

        self.stack = SortedContextStack(self.inner)

    def test_init_requires_one_arg(self):
        self.assertRaises(TypeError, SortedContextStack)

    def test_pop_calls_inner_stack(self):
        self.stack.pop()
        self.inner.pop.assert_called_once_with()

    def test_push_calls_inner_stack(self):
        self.stack.push(dict(a=1))
        self.inner.push.assert_called_once_with(dict(a=1))

    def test_str_calls_inner_stack_and_does_not_manipulate_output(self):
        out = str(self.stack)
        self.inner.__str__.assert_called_once_with()
        self.assertEqual("foo", out)

    def test_iter_calls_inner_iterable(self):
        iter(self.stack)
        self.inner.__iter__.assert_called_once_with()

    def test_iter_returns_sorted_iterable(self):
        items = iter(self.stack)
        self.inner.__iter__.assert_called_once_with()

        self.assertEquals(list(items), [("a", 2), ("a", 1), ("b", 1)])

