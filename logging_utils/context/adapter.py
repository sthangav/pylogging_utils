# -*- coding: utf-8 -*-
""" Package contains logging adapter """
import logging
from contextlib import contextmanager


class LoggerAdapterWithContext(logging.LoggerAdapter):
    """ Logger subclass that allows to define context.
    IT IS NEITHER THREAD NOR ASYNC SAFE
    """

    def __init__(self, stack, logger):
        """ Object initializator

        :param stack: context stack to be used
        :type stack: logging_utils.context.stack
        :param logger: inner (decoratee) logger instance
        :type logger: logging.Logger
        :returns: new instance of self
        :rtype: logging_utils.context.LoggerContextual
        """
        self._stack = stack
        return super(LoggerAdapterWithContext, self).__init__(logger, None)

    @contextmanager
    def context(self, **kwargs):
        """ Returns current (most-recently created) context

        :returns: instance of logging context
        :rtype: logging_utils.context.LoggerContextual
        """
        self._stack.push(kwargs)
        try:
            yield self
        finally:
            self._stack.pop()

    def process(self, msg, kwargs):
        """ Process log message before write them into log

        :param msg: message to be written into log
        :type msg: str
        :param kwargs: additional arguments to be logged along with message
        :type kwargs: dict
        :returns: tuple containing pre-processed msg and kwargs
        :rtype: tuple
        """
        return super(LoggerAdapterWithContext, self).process(
            '; '.join([msg, str(self._stack)]), kwargs)

