import sys
import os
import yaml
import logging
import types

from .misc import Config

"""
The common.py script is where all globally accessable variables and instances
are set up.
"""


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
