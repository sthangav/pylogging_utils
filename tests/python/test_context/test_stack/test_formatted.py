# encoding: utf-8
import unittest

from logging_utils._compat import mock
from logging_utils.context.stack.formatted import KeyValueFormattedContextStack


class KeyValueFormattedContextStackTest(unittest.TestCase):

    def setUp(self):
        self.inner = mock.MagicMock(spec=KeyValueFormattedContextStack)
        self.inner.__str__.return_value = "foo"
        self.inner.__iter__.return_value = [("b", 1), ("a", 2), ("a", 1)]

        self.stack = KeyValueFormattedContextStack(self.inner)

    def test_init_requires_one_arg(self):
        self.assertRaises(TypeError, KeyValueFormattedContextStack)

    def test_pop_calls_inner_stack(self):
        self.stack.pop()
        self.inner.pop.assert_called_once_with()

    def test_push_calls_inner_stack(self):
        self.stack.push(dict(a=1))
        self.inner.push.assert_called_once_with(dict(a=1))

    def test_str_only_formats_inner_values_and_does_not_reorder(self):
        out = str(self.stack)
        self.assertEqual(out, '[b]=[1]; [a]=[2]; [a]=[1]')

    def test_iter_calls_inner_iterable(self):
        iter(self.stack)
        self.inner.__iter__.assert_called_once_with()

    def test_iter_returns_value_from_inner_iterable_as_is(self):
        items = iter(self.stack)
        self.inner.__iter__.assert_called_once_with()

        self.assertEquals(list(items), [("b", 1), ("a", 2), ("a", 1)])

