
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
		raise TypeError('Instance not expected type')

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
	check_type(exception_type, Exception)
	check_type(class_name, StringType)
	check_type(message, StringType)
	check_type(debug_info, DictType)
	return exception_type('%s: "%s"', class_name, message, args=debug_info)

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
		logger.warning(log_format_error(e, 'Result missing from function call X'), exc_info=True)
	"""
	check_type(event_str, StringType)
	check_type(data, DictType)
	info = ''
	for k, v in data:
		info += format('%s: %s, ', k, v)
	return format('%s. Info: (%s)', event_str, info)

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
	debug = '\n'
	for k, v in caught_exception.args:
		debug += format('%s: `%s`\n', k, v)
	return format('%s (%s) - debug: %s', event_str, caught_exception, debug)
