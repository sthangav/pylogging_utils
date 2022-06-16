# -*- coding: utf-8 -*-

from logging_utils._compat import map

class KeyValueFormattedContextStack(object):

    def __init__(self, inner):
        self._stack = inner
        self._format_context_arg = lambda tpl: "[{0}]=[{1}]".format(tpl[0], tpl[1])

    def push(self, context):
        self._stack.push(context)
        return self

    def pop(self):
        self._stack.pop()
        return self

    def __iter__(self):
        return iter(self._stack)

    def __str__(self):
        return '; '.join(map(self._format_context_arg, self))

