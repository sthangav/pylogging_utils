# -*- coding: utf-8 -*-
"""
Python 2.7.x, 3.2+ compatability module.
"""
from __future__ import unicode_literals
import operator
import sys

is_py2 = sys.version_info[0] == 2

if not is_py2:
    # Python 3

    # lazy iterators
    map = map
    iteritems = operator.methodcaller('items')
else:
    # Python 2

    # lazy iterators
    from itertools import imap
    map = imap
    iteritems = operator.methodcaller('iteritems')

# try to import "mock" (built-in Py3, external module in Py2)
try:
    from unittest import mock as _mock
    mock = _mock
except ImportError:
# mock is required only for tests - it might not be available for regular use
    try:
        import mock
    except ImportError:
        pass

__all__ = ['map', 'iteritems', 'mock']

