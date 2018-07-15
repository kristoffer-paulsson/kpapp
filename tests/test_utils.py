import unittest
import types

from kpapp.utils import check_type, format_exception, log_format_info, log_format_error

class TestCheckType(unittest.TestCase):

    def test_int(self):
        try:
            check_type(23343, types.IntType)
        except TypeError as e:
            self.assertTrue(e == False)
        self.assertTrue(True, True)

    def test_str(self):
        try:
            check_type('Hello world', types.StringType)
        except TypeError as e:
            self.assertTrue(TypeError == False)
        self.assertTrue(True == True)

    def test_class(self):
        self.assertRaises(TypeError, 'check_type', instance=RuntimeError(), type=Exception)

class TestCheckClass(unittest.TestCase):

    def test_int(self):
        self.assertRaises(TypeError, 'check_class', instance=54353, type=types.StringType)

    def test_class(self):
        self.assertRaises(TypeError, 'check_class', instance=RuntimeError(), type=Exception)

class TestFormatException(unittest.TestCase):

    def test_format(self):
        debug = {
            'id': 45654654767,
            'user': 'User Name'
        }
        e = format_exception(
            RuntimeError,
            self.__class__.__name__,
            'Unexpected result',
            debug
        )
        self.assertTrue(str(e) == 'TestFormatException, "Unexpected result" - debug: (id: 45654654767, user: User Name)')

class TestLogFormatInfo(unittest.TestCase):

    def test_format_success(self):
        data = {
            'id': 45654654767,
            'user': 'User Name'
        }
        str = log_format_info('Business transaction complete', data)
        self.assertTrue(str == 'Business transaction complete. Info: id: 45654654767, user: User Name')

    def test_format_wrong(self):
        data = {
            'id': 45654654767,
            'user': 'User Name'
        }
        str = log_format_info('Business transaction complete', data)
        self.assertFalse(str == 'Business transaction complete. Info: id: 45654654767')

class TestLogFormatError(unittest.TestCase):

    def test_format_success(self):
        debug = {
            'id': 45654654767,
            'user': 'User Name'
        }
        e = format_exception(
            RuntimeError,
            self.__class__.__name__,
            'Unexpected result',
            debug
        )

        str_res = log_format_error(e, 'Business transaction failed')
        self.assertTrue(str_res == 'Business transaction failed, Class: <type \'exceptions.RuntimeError\'>:TestLogFormatError, "Unexpected result" - debug: (id: 45654654767, user: User Name)')

    def test_format_wrong(self):
        debug = {
            'id': 45654654767,
            'user': 'User Name'
        }
        e = format_exception(
            RuntimeError,
            self.__class__.__name__,
            'Business transaction failed',
            debug
        )

        str_res = log_format_error(e, 'Business transaction failed')
        self.assertFalse(str_res == 'Business transaction complete, Class: <type \'exceptions.RuntimeError\'>:TestLogFormatError, "Unexpected result" - debug: (id: 45654654767, user: User Name)')

if __name__ == '__main__':
    unittest.main()
