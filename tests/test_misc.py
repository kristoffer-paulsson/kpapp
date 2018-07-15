import unittest
import types
import os
import shutil
import tempfile

from kpapp.misc import Config

test_yaml = """
---
hello: world
foo: bar
baz: qwerty
"""

class TestConfig(unittest.TestCase):
    __config = None
    __test_path = ''

    def setUp(self):
        self.__config = Config()
        self.__test_path = tempfile.mkdtemp()
        f = file(self.__test_path + '/test.yaml', 'w+')
        f.write(test_yaml)
        f.close()


    def tearDown(self):
        del self.__config
        shutil.rmtree(self.__test_path)

    def test_load(self):
        immutable = {
            'hello': 'galaxy'
        }
        default = {
            'foo': 100,
            'baz': 200,
            'star': 'sun'
        }
        result = {
            'baz': 'qwerty',
            'foo': 'bar',
            'star': 'sun',
            'hello': 'galaxy'
        }
        merged =  self.__config.load(
            self.__test_path + '/test.yaml',
            default,
            immutable
        )
        self.assertTrue(set(merged.keys()) == set(result.keys()))
        self.assertTrue(set(merged.values()) == set(result.values()))

    def test_usr(self):
        self.assertTrue(os.path.exists(self.__config.usr_dir()))

    def test_app(self):
        self.assertTrue(os.path.exists(self.__config.app_dir()))

    def test_exe(self):
        self.assertTrue(os.path.exists(self.__config.exe_dir()))

if __name__ == '__main__':
    unittest.main()
