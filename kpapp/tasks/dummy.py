#import time
from ..task import Task

class Dummy(Task):
	NAME = 'Dummy'
	def __init__(self, sig):
		Task.__init__(self, self.NAME, sig)
		self.__count = 0
		
	def work(self):
		self.__count += 1
		print 'Task "' + self.name() + '" loop ' + str(self.__count)
		self._idle(1)