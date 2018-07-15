from types import *
"""
The utils.py module is the module that containse all minor extras that is used
globally in the application
"""

def check_type(instance, type):
	"""
	check_type is a helper function. Tests for an instance and raises a
	standardized TypeError exception.

	Instance	The instanced variable
	type		The class type of expected type, or tuple of them

	Example:
	check_type(result, (NoneType, StringType))
	"""
	if not isinstance(instance, type):
		raise TypeError('Instance expected type {0}, but got: {1}', type(type),  type(instance))

def check_class(instance, type):
	"""
	check_class is a helper function. Tests for a subclass and raises a
	standardized TypeError exception.

	Instance	The instanced variable
	type		The class type of expected type, or tuple of them

	Example:
	check_class(result, (Model, BaseModel))
	"""
	if not issubclass(instance, type):
		raise TypeError('Subclass expected type {0}, but got: {1}', type(type), type(instance))

def format_exception(exception_type, class_name = 'No classname', message = 'Formated exception', debug_info = {}):
	"""
	format_exception is a helper function. It will populate and format an
	exception so that it is understandable and include good debug data.

	exception_type		Requiers an exception type
	class_name			The class name of current class, or of current instance
	message				Simple error message
	debug_info			A dictionary of interesting debug values
	returns				A string to enter into exception

	Example:
	raise format_exception(
		RuntimeError,
		self.__class__.__name__,
		'Unexpected result',
		{
			id: 45654654767,
			user: 'User Name'
		}
	)
	"""
	check_class(exception_type, Exception)
	check_type(class_name, StringType)
	check_type(message, StringType)
	check_type(debug_info, DictType)

	debug = []
	for k in debug_info:
		debug.append('{0}: {1}'.format(k, debug_info[k]))
	exc =  exception_type('{0}, "{1}" - debug: ({2})'.format(class_name, message, ', '.join(debug)))
	return exc

def log_format_info(event_str, data = {}):
	"""
	log_format_info is a helper function. It will format an info message with
	support for event data.

	event_str			A string describing the event
	data				A dictionary with info
	returns				string to pass to logger.info()

	Example:
	try:
		...
	except Exception as e:
		logger.warning(log_format_info(e, 'Result missing from function call X'), exc_info=True)
	"""
	check_type(event_str, StringType)
	check_type(data, DictType)

	info = []
	for k in data:
		info.append('{0}: {1}'.format(k, data[k]))
	return '{0}. Info: {1}'.format(event_str, ', '.join(info))

def log_format_error(caught_exception, event_str):
	"""
	log_format_error is a helper function. It will format an exception and message
	formatted with help of format_exception().

	caught_exception	An exception
	event_str			A string describing the event
	returns				string to pass to logger.error()

	Example:
	try:
		...
	except Exception as e:
		logger.warning(log_format_error(e, 'Result missing from function call X'), exc_info=True)
	"""
	check_type(caught_exception, Exception)
	check_type(event_str, StringType)
	
	return '{0}, Class: {1}:{2}'.format(event_str, str(type(caught_exception)), caught_exception)
