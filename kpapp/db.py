import importlib
import threading
from peewee import SqliteDatabase, Database as PWDatabase
from .service import Service
from .common import conf

"""
The db.py module containes application wrappers and helper classes to work with
databases within the application such as the Database wrapper class and the
DatabaseManager class.
"""

class Database:
	"""
	A Database wrapper for Database and ORM connection for peewee.
	"""
	def __init__(self, db):
		#, peewee.SqliteDatabase, peewee.MySQLDatabase, peewee.PostgresqlDatabase)
		if not isinstance(db, PWDatabase):
			raise TypeError
		self.__db = db
		self.__lock = threading.Lock()

	def get(self):
		return self.__db

	def lock(self):
		self.__lock.acquire()

	def unlock(self):
		self.__lock.release()

class DatabaseManager(Service):
	"""
	Databasemanager service for the Application
	"""
	NAME = 'DatabaseManager'
	def __init__(self, config = {}):
		Service.__init__(self, self.NAME, config)

		self.__instances = {}

	def __instantiate(self, name):
		if not self.__instances.has_key(name):
			c = self._config()
			cc = c[name]
			if not cc.has_key('type'):
				raise RuntimeError('Database connection "' + str(name) + '" must configure "type".')

			if not cc.has_key('class'):
				raise RuntimeError('Database connection "' + str(name) + '" must configure "class".')

			try:
				pkg = cc['class'].rsplit('.',1)
				klass = getattr(importlib.import_module(pkg[0]), pkg[1])
			except ImportError:
				raise RuntimeError('Database class "' + str(cc['class']) + '" not found.')

			if cc['type'] == 'sqlite':
				conn = SqliteDatabase(conf.app_dir() + cc['path'])
				db = klass(conn)
				if not isinstance(db, Database):
					raise TypeError('Database connection "' + str(name) + '" "package" not of type Database.')
			else:
				raise RuntimeError('Database connection "' + str(name) + '" "type" value is invalid.')

			self.__instances[name] = db

		return self.__instances[name]

	def get(self, name):
		if not self._config().has_key(name):
			raise RuntimeError('Database connection "' + str(name) + '" not configured.')
		else:
			return self.__instantiate(name)
