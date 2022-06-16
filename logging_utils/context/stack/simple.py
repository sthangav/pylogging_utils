# -*- coding: utf-8 -*-

from itertools import chain
from logging_utils._compat import iteritems, map

class SimpleContextStack(object):

    def __init__(self):
        self._stack = []

    def push(self, context):
        self._stack.append(context)
        return self

    def pop(self):
        self._stack.pop()
        return self

    def __iter__(self):
        return iter(iteritems(dict(chain.from_iterable(map(iteritems, self._stack)))))

    def __str__(self):
        return str(self._stack)

