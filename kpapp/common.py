import sys
import os
import yaml
import logging

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

conf = Config()

class Log():
	def __init__(self, config = {}):
		pass

	def logger(self):
		logger = logging.getLogger('app')
		hdlr = logging.FileHandler(conf.app_dir() + '/data/log/error.log', mode='a+')
		formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
		hdlr.setFormatter(formatter)
		logger.addHandler(hdlr)
		logger.setLevel(logging.DEBUG)
		return logger

	def bizz(self):
		logger = logging.getLogger('biz')
		hdlr = logging.FileHandler(conf.app_dir() + '/data/log/bizz.log', mode='a+')
		formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
		hdlr.setFormatter(formatter)
		logger.addHandler(hdlr)
		logger.setLevel(logging.DEBUG)
		return logger

logger = Log({}).logger()
bizz = Log({}).bizz()
