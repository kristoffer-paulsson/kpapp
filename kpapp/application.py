import time
import os
import sys
import atexit
from signal import SIGTERM

from .common import conf, logger
from .task import TaskManager
from .tasks.dummy import Dummy
from .db import DatabaseManager

"""
The application.py module containes all classes needed for the major execution
and running of the application, such as the Application class and the
Daemonizer
"""

class Application:
	"""
	Main Application class. This class should be subclassed for every new
	application being made. Subclassed versions should define container methods
	for services.
	"""
	def __init__(self, config = {}):
		"""
		Initializes the Application with application wide condig values.
		config		Dictionary of key/value pairs
		"""
		if not isinstance(config, dict):
			raise TypeError('config not dict')
		# Apps config data
		self.__config = config
		# A dictionary of service objects
		self.__services = {}

	def _initialize(self):
		"""
		Things to be done prior to main process loop execution. This method
		should be overriden.
		"""
		tm = self.task_manager()
		tm.setup(Dummy(tm.get_signal()))

	def _finalize(self):
		"""
		Things to be done after main process loop execution. This method can be
		overriden. Don't forget to stop the TaskManager.
		"""
		self.task_manager().stop()

	def run(self, mode = 'default'):
		"""
		The main loop and thread of the application. Supports Ctrl^C key
		interruption, should not be overriden. Also handles major unexpected
		exceptions and logs them as CRITICAL.
		"""
		logger.info('========== Begin execution of program ==========')
		try:
			self._initialize()
			try:
				while True:
					time.sleep(1)
			except KeyboardInterrupt:
				pass
			self._finalize()
		except Exception as e:
			logger.critical('Application.run(), Unhandled exception: (%s)', str(e), exc_info=True)
			sys.exit('########## Program crash due to internal error ##########')
		logger.info('========== Finish execution of program ==========')

	def _service(self, name, service):
		"""
		Helper method to instantiate a Service IoC style
		name 		The "name" of the Service
		service		The service object itself
		"""
		if name in self.__services:
			return self.__services[name]
		else:
			logger.debug('Instanciating service: %s', name)
			self.__services[name] = service(self)
			return self.__services[name]

	def _config(self, name):
		"""
		Returns a main section of the application wide key/value pairs
		configuration.
		name		The section name, usually a Service name.
		"""
		if not self.__config.has_key(name):
			logger.error('Config section missing: %s', name)
			raise RuntimeError('Config section "' + name +  '" missing')
		return self.__config[name]

	def task_manager(self):
		"""
		IoC implementation of the TaskManager, returns the one instance of
		task manager.
		"""
		def service(self):
			return TaskManager()
		return self._service(TaskManager.NAME, service)

	def database_manager(self):
		"""
		IoC implementation of the TaskManager, returns the one instance of
		task manager.
		"""
		def service(self):
			return DatabaseManager(self._config(DatabaseManager.NAME))
		return self._service(DatabaseManager.NAME, service)

class Daemonizer:
	"""
	An Application daemonizer

	Usage: daemonize a subclassed Application class
	"""
	def __init__(self, app, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
		self.__app = app
		self.__stdin = stdin
		self.__stdout = stdout
		self.__stderr = stderr
		self.__pidfile = pidfile

	def __daemonize(self):
		"""
		do the UNIX double-fork magic, see Stevens' "Advanced
		Programming in the UNIX Environment" for details (ISBN 0201563177)
		http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
		"""
		try:
			pid = os.fork()
			if pid > 0:
				# exit first parent
				sys.exit(0)
		except OSError, e:
			sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
			sys.exit(1)

		# decouple from parent environment
		os.chdir("/")
		os.setsid()
		os.umask(0)

		# do second fork
		try:
			pid = os.fork()
			if pid > 0:
				# exit from second parent
				sys.exit(0)
		except OSError, e:
			sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
			sys.exit(1)

		# redirect standard file descriptors
		sys.stdout.flush()
		sys.stderr.flush()
		si = file(self.__stdin, 'r')
		so = file(self.__stdout, 'a+')
		se = file(self.__stderr, 'a+', 0)
#		os.dup2(si.fileno(), sys.stdin.fileno())
#		os.dup2(so.fileno(), sys.stdout.fileno())
#		os.dup2(se.fileno(), sys.stderr.fileno())

		# write pidfile
		atexit.register(self.__delpid)
		pid = str(os.getpid())
		file(self.__pidfile,'w+').write("%s\n" % pid)

	def __delpid(self):
		os.remove(self.__pidfile)

	def start(self, daemonize = True):
		"""
		Start the daemon
		"""
		# Check for a pidfile to see if the daemon already __runs
		try:
			pf = file(self.__pidfile,'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None

		if pid:
			message = "pidfile %s already exist. Daemon already running?\n"
			sys.stderr.write(message % self.__pidfile)
			sys.exit(1)

		# Start the daemon
		if daemonize:
			self.__daemonize()
		self.__app.run()

	def stop(self):
		"""
		Stop the daemon
		"""
		# Get the pid from the pidfile
		try:
			pf = file(self.__pidfile,'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None

		if not pid:
			message = "pidfile %s does not exist. Daemon not running?\n"
			sys.stderr.write(message % self.__pidfile)
			return # not an error in a restart

		# Try killing the daemon process
		try:
			while 1:
				os.kill(pid, SIGTERM)
				time.sleep(0.1)
		except OSError, err:
			err = str(err)
			if err.find("No such process") > 0:
				if os.path.exists(self.__pidfile):
					os.remove(self.__pidfile)
			else:
				print str(err)
				sys.exit(1)

	def restart(self):
		"""
		Restart the daemon
		"""
		self.stop()
		self.start()
