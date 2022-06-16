# -*- coding: utf-8 -*-

from collections import ChainMap
from logging_utils._compat import iteritems

class ChainMapContextStack(object):

    def __init__(self):
        self._stack = ChainMap()

    def push(self, context):
        self._stack = ChainMap(context, *self._stack.maps)
        return self

    def pop(self):
        self._stack = self._stack.parents
        return self

    def __iter__(self):
        return iter(iteritems(self._stack))

    def __str__(self):
        return str(self._stack)

