import os
import sys
import types
import yaml

from .utils import check_type

class Config:
	__app_path = os.path.dirname(os.path.abspath(sys.argv[0]))
	__usr_path = os.path.expanduser('~')
	__exe_path = os.path.abspath(os.getcwd())

	def __init__(self):
		self.__config = None

	def load(self, path, default = {}, immutable = {}):
		"""
		Loads configuration from disk. But can be prepended with a hardcoded
		default configuration and postpended with an immutable hardcoded
		configuration. Loaded config overrides default values and immutable
		config overrides loaded values.
		path		String with path to config yaml file
		default		Prepended default config
		immutable	Postpended immutable config
		"""
		check_type(path, types.StringType)
		check_type(default, types.DictType)
		check_type(immutable, types.DictType)
		if not os.path.exists(path):
			raise ValueError('Path is not an existing file.')

		if not bool(self.__config):
			f = file(path, 'r')
			config = yaml.load(f)
			f.close()

			d = default.copy()
			d.update(config)
			i = d.copy()
			i.update(immutable)
			self.__config = i
		return self.__config

	def app_dir(self):
		"""
		Absolute path to the executed scripts location.
		"""
		return self.__app_path

	def usr_dir(self):
		"""
		Absolute path to user home directory.
		"""
		return self.__usr_path

	def exe_dir(self):
		"""
		Absolute path to current working directory.
		"""
		return self.__exe_path
