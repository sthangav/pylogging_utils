# encoding: utf-8

class Sentinel(object):

    def __init__(self, logger, message, reraise=True, with_traceback=True,
                 log_success=True):
        """ Object initialization

        :param logger: logger to be used to log messages
        :type logger: logging.Logger
        :param message: message to be logged
        :type message: str
        :param reraise: whether to re-raise exceptions when occur
        :type raraise: bool
        :param with_traceback: whether to append or not exception traceback
            when logging 'critical' case
        :type with_traceback: bool
        :param log_success: whether to log success or not when exiting context
            without any exception and any other calls to sentinel
        :type log_success: bool
        """
        self._logger = logger
        self._message = message
        self._reraise = bool(reraise)
        self._with_traceback = bool(with_traceback)
        self._log_success = bool(log_success)
        self._called = False

    def success(self):
        """ Logs success (using INFO level) with predefined message """
        self._called = True
        self._logger.info(self._message)

    def failure(self):
        """ Logs failure (using ERROR level) without traceback """
        self._called = True
        self._logger.error(self._message)

    def critical(self, exc_info=None):
        """ Logs critical (using EXCEPTION level) with additional exception traceback

        :param exc_info: optional exception traceback. See :py:func:Sentinel._get_exc_info
        :type exc_info: tuple
        """
        self._called = True
        self._logger.exception(self._message, exc_info=self._get_exc_info(exc_info))

    def _get_exc_info(self, exc_info):
        """ Returns exception traceback according to internal configuration
        and given exc_info paramter

        If traceback was not allowed (see: with_traceback) it will be NOT added,
        despite of exc_info provided. If traceback was requested and exc_info
        contains tuple it will be used as traceback information. Otherwise
        logging module will be requested to obtain and append traceback on it's own
        (default behaviour is to call :py:func:sys.exc_info)

        :param exc_info: optional exception traceback
        :type exc_info: tuple
        """
        if not self._with_traceback:
            return False
        if isinstance(exc_info, tuple):
            return exc_info
        return True

    def _log_success_if_needed(self):
        """ Helper function to decide whether to log "success" or not
        Used in __exit__ method """
        if self._called:
            return
        if not self._log_success:
            return
        self.success()

    def __enter__(self):
        """ Enters context

        :returns: self
        :rtype: Sentinel
        """
        return self

    def __exit__(self, exc_type, exc_value, exc_info):
        if exc_type is None:
            self._log_success_if_needed()
            return

        self.critical(exc_info)

        return not self._reraise

class SentinelBuilder(object):
    """ Builds instances of Sentinel class with predefined parameters """

    SENTINEL_CLASS = Sentinel

    def __init__(self, logger, reraise=True, with_traceback=True,
                 log_success=True):
        """ Object initialization

        :param logger: logger to be used to log messages
        :type logger: logging.Logger
        :param reraise: whether to re-raise exceptions when occur
        :type raraise: bool
        :param with_traceback: whether to append or not exception traceback
            when logging 'critical' case
        :type with_traceback: bool
        :param log_success: whether to log success or not when exiting context
            without any exception and any other calls to sentinel
        :type log_success: bool
        """
        self._logger = logger
        self._reraise = bool(reraise)
        self._with_traceback = bool(with_traceback)
        self._log_success = bool(log_success)

    def __call__(self, message, logger=None, reraise=None, with_traceback=None,
                 log_success=None):
        """ Creates Sentinel instances. Allows to override some of the
        predefined parameters """
        return self.SENTINEL_CLASS(logger or self._logger, message,
                        reraise or self._reraise,
                        with_traceback or self._with_traceback,
                        log_success or self._log_success)

