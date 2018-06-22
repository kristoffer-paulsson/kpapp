class Service:
	"""
	Service is a base class for Application services.
	"""
	def __init__(self, name, config = {}, conf_vars = []):
		if not isinstance(name, basestring):
			raise TypeError('"name" must be basestring')
		if not isinstance(config, dict):
			raise TypeError('"config" must be dict')
		if not isinstance(conf_vars, list):
			raise TypeError('"conf_vars" must be list')

		self.__name = name
		self.__config = config
		# Implement support for services to define accepted variables
		self.__vars = conf_vars

	def service(self):
		raise NotImplementedError()

	def _config(self, name = ''):
		if not bool(name):
			return self.__config
		elif self.__config.has_key(name): #and name in self.__vars
			return self.__config[name]
		else:
			return None

	def name(self):
		return self.__name
