import threading
import time
import sys
from .common import logger
from .service import Service

"""
The task.py module containes classes needed to manage multithreading and running
tasks within the application.
"""

class Signal:
	"""
	Signal class is used by the TaskManager to communicate with the Task
	classes.
	"""
	def __init__(self, halt, run):
		"""
		halt	threading.Event signaling halt to all the Task threads
		run		threading.Event signaling pause/resume to all Task threads
		"""
		self.__run = run
		self.__halt = halt

	def halt(self):
		"""
		Returns the state of the halt signal
		"""
		return self.__halt.is_set()

	def pause(self):
		"""
		Will make calling thread pause until resume signal
		"""
		self.__run.wait()

class Task:
	"""
	Task class is a wrapper for threads. The task keeps track of signals and
	contains _initialize(), _finalize() and run() methods. In order to Implement
	a task, Task should be subclassed and work() implemented.
	"""
	def __init__(self, name, sig, config = {}):
		"""
		name 	A string with the Task name
		sig		The Signal class instance to listen too
		config	A dictionary with config values
		"""
		if not isinstance(name, basestring):
			raise TypeError('name not basestring')
		if not isinstance(config, dict):
			raise TypeError('config not dict')
		if not isinstance(sig, Signal):
			raise TypeError('sig not Signal')

		self.__name = name
		self.__sig = sig
		self.__config = config
		self.__done = False
		self.__idle = 0

	def name(self):
		"""
		Returns task name.
		"""
		return self.__name

	def _idle(self, seconds):
		"""
		Instructs the run() method to sleep for "seconds" seconds.
		"""
		self.__idle = int(seconds)

	def _config(self):
		"""
		Returns initiated config values dictionary.
		"""
		return self.__config

	def _done(self):
		"""
		Instructs the run() method to exit thread.
		"""
		self.__done = True

	def _initialize(self):
		"""
		Overridable method that the run() method executes before entering the
		work loop.
		"""
		pass

	def _finalize(self):
		"""
		Overridable method that the run() method executes after exiting the
		work loop.
		"""
		pass

	def run(self, args = {}):
		"""
		The run() method that is used as thread. Contains the logic to run the
		task and listen to signals. This method should not be overriden. It also
		catches all uncaught exceptions and logs them as CRITICAL with
		traceback. It is recommended to not handle unexpected exceptions, but
		lets the task report them in a standardized manner.
		"""
		try:
			self._initialize()
			while not (self.__sig.halt() or self.__done):
				self.__sig.pause()
				if self.__idle > 0:
					self.__idle -= 1
					time.sleep(1)
				else:
					self.work()
			self._finalize()
		except:
			logger.critical('Task.run(), Unhandled exception: (%s)', self.__name, exc_info=True)
			sys.exit('########## Program crash due to internal error ##########')
		logger.info('Thread %s has gracefully halted', self.__name)

	def work(self):
		"""
		The Tasks business logic should be implemented in the work() method.
		"""
		raise NotImplementedError

class TaskGroup:
	"""
	TaskGroup is to be implemented. With TaskGroup you should be able to
	instantiate, monitor and communicate with Tasks in groups.
	"""
	pass

class TaskManager(Service):
	"""
	TaskManag is the Application Service that handles multithreading and
	interthread communications
	"""
	NAME = 'TaskManager'
	KILL_RANGE = 10
	def __init__(self):
		"""
		Instantiates and initializes the TaskManager setting up interthread
		communication.
		"""
		Service.__init__(self, self.NAME)
		self.__tasks = {}

		self.__run = threading.Event()
		self.__run.set()
		self.__halt = threading.Event()
		self.__halt.clear()

		self.__signal = Signal(run=self.__run, halt=self.__halt)

	def get_signal(self):
		"""
		Returns the internal Signal class.
		"""
		return self.__signal

	def suspend(self):
		"""
		Pauses the threads by setting the "run" signal to False.
		"""
		self.__run.clear()

	def resume(self):
		"""
		Resumes the paused threads by setting the "run" signal to True.
		"""
		self.__run.set()

	def stop(self):
		"""
		Halts all the threads by setting the run signal to False. Then cleans
		up all the threads.
		"""
		logger.info('Halt all threads')
		self.__halt.set()
		self.__run.set()

		for i in range(TaskManager.KILL_RANGE):
			if threading.active_count() > 1:
				time.sleep(1)
			else:
				logger.info('All threads halted')
				return True
		logger.error('Couldn\'t halt all threads')
		return False

	def setup(self, task, args = {}):
		"""
		Registers a Task and initializes a thread for the run() method.
		"""
		if not isinstance(task, Task):
			raise TypeError('Not a Task')
		elif task.name() in self.__tasks:
			raise RuntimeError('Task already exists')
		else:
			logger.info('Starting thread: %s', task.name())
			self.__tasks[task.name()] = task
			thread = threading.Thread(target=task.run, name=task.name(), args=args)
			thread.start()
			logger.info('Thread started: %s', task.name())
