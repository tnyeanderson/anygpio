# Error definitions
class SystemNotSet(Exception):
	"""
	Thrown when GPIO.system is not set
	"""
	pass

class WrongPinType(Exception):
	"""
	Thrown when trying to output() to an input pin, and vice versa
	"""
	pass

class NoNativeGPIO(Exception):
	"""
	Thrown when there is no Native GPIO python library installed

	Example: RPi.GPIO is not installed
	"""
	pass

class WrapperError(Exception):
	"""
	Generic exception regarding GPIO wrapper
	"""
	pass

class GPIOFunctionNotSupported(Exception):
	"""
	Generic exception regarding GPIO function support
	"""
	pass
