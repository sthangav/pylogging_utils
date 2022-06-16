import logging
from .adapter import LoggerAdapterWithContext

_ContextStack = None
try:
    from .stack.chainmap import ChainMapContextStack
    _ContextStack = ChainMapContextStack
except:
    from .stack.simple import SimpleContextStack
    _ContextStack = SimpleContextStack

from .stack.sorted import SortedContextStack
from .stack.formatted import KeyValueFormattedContextStack


def buildFormattedAndSortedContextStack():
    return KeyValueFormattedContextStack(SortedContextStack(_ContextStack()))

DEFAULT_CONTEXT_STACK = buildFormattedAndSortedContextStack()

def getLoggerWithContext(*args, **kwargs):
    return LoggerAdapterWithContext(
        DEFAULT_CONTEXT_STACK,
        logging.getLogger(*args, **kwargs)
    )

