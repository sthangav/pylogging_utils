# encoding: utf-8

import logging
import unittest

from logging_utils._compat import mock

from logging_utils.sentinel import Sentinel, SentinelBuilder

class SentinelBuilderTest(unittest.TestCase):

    def setUp(self):
        self.sentinel_class = mock.MagicMock()
        self.logger = mock.MagicMock()
        self.builder = SentinelBuilder(self.logger, reraise=False,
                                       with_traceback=False, log_success=False)
        self.builder.SENTINEL_CLASS = self.sentinel_class

    def test_builder_returns_instance_of_sentinel(self):
        self.builder.SENTINEL_CLASS = Sentinel
        self.assertIsInstance(self.builder('foo'), Sentinel)

    def test_builder_uses_predefined_values(self):
        self.builder('foo')
        self.sentinel_class.assert_called_once_with(self.logger, 'foo', False,
                                                    False, False)

    def test_builder_allows_to_override_predefined_values(self):
        logger = mock.MagicMock()
        self.builder('foo', logger)
        self.sentinel_class.assert_called_once_with(logger, 'foo', False,
                                                    False, False)
        self.sentinel_class.reset_mock()

        self.builder('foo', reraise=True)
        self.sentinel_class.assert_called_once_with(self.logger, 'foo', True,
                                                    False, False)
        self.sentinel_class.reset_mock()

        self.builder('foo', with_traceback=True)
        self.sentinel_class.assert_called_once_with(self.logger, 'foo', False,
                                                    True, False)
        self.sentinel_class.reset_mock()

        self.builder('foo', log_success=True)
        self.sentinel_class.assert_called_once_with(self.logger, 'foo', False,
                                                    False, True)
        self.sentinel_class.reset_mock()

class SentinelTest(unittest.TestCase):

    def setUp(self):
        self.logger = mock.MagicMock(spec=logging.Logger)
        self.message = 'foo'
        self.reraise = True
        self.with_traceback = True
        self.log_success = True

    def sentinel(self):
        """ Returns new instance of sentinel

        :rtype: Sentinel
        """
        return Sentinel(self.logger, self.message, self.reraise,
                        self.with_traceback, self.log_success)

    def test_success_logs_info_message(self):
        self.sentinel().success()
        self.logger.info.assert_called_once_with(self.message)

    def test_failure_logs_error_message(self):
        self.sentinel().failure()
        self.logger.error.assert_called_once_with(self.message)

    def test_critical_logs_exception_message(self):
        self.with_traceback = False
        self.sentinel().critical()
        self.logger.exception.assert_called_once_with(self.message, exc_info=False)

    def test_critical_can_request_traceback(self):
        self.sentinel().critical()
        self.logger.exception.assert_called_once_with(self.message, exc_info=True)

    def test_critical_uses_given_traceback(self):
        tb = ('foo', )
        self.sentinel().critical(tb)
        self.logger.exception.assert_called_once_with(self.message, exc_info=tb)

    def test_critical_can_suppress_any_traceback(self):
        self.with_traceback = False
        tb = ('foo', )
        self.sentinel().critical(tb)
        self.logger.exception.assert_called_once_with(self.message, exc_info=False)

    def test_context_can_suppress_exceptions_but_logs_failure(self):
        self.reraise = False
        with self.sentinel():
            raise RuntimeError()
        self.logger.exception.assert_called_once_with(self.message, exc_info=True)

    def test_context_can_re_raise_exceptions_but_logs_failure(self):
        with self.assertRaises(RuntimeError):
            with self.sentinel():
                raise RuntimeError()
        self.logger.exception.assert_called_once_with(self.message, exc_info=True)

    def test_context_logs_failures(self):
        with self.sentinel() as sentinel:
            sentinel.failure()
        self.logger.error.assert_called_once_with(self.message)

    def test_context_might_automatically_log_success(self):
        with self.sentinel():
            pass

        self.logger.info.assert_called_once_with(self.message)

    def test_context_does_not__automatically_log_success_in_case_of_failure(self):
        with self.sentinel() as sentinel:
            sentinel.failure()

        self.assertEqual(0, self.logger.info.call_count)

    def test_context_does_not__automatically_log_success_in_case_of_exception(self):
        self.reraise = False

        with self.sentinel():
            raise RuntimeError()

        self.assertEqual(0, self.logger.info.call_count)

    def test_context_does_not_automatically_log_success_if_already_logged(self):
        with self.sentinel() as sentinel:
            self.assertEqual(0, self.logger.info.call_count)
            sentinel.success()
            self.logger.info.assert_called_once_with(self.message)

        self.logger.info.assert_called_once_with(self.message)

    def test_context_does_not_automatically_log_success_if_not_requested(self):
        self.log_success = False

        with self.sentinel():
            pass

        self.assertEqual(0, self.logger.info.call_count)

