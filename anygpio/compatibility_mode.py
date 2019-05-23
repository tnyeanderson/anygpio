class _GPIO():
	"""
	Provides cross-platform support for RPi-like API calls

	self.wrapper provides access to the wrapper used by the system
	"""
	wrapper = None

	@property
	def BOTH(self):
		return self.wrapper._native_both()

	@property
	def FALLING(self):
		return self.wrapper._native_rising_falling(0)

	@property
	def RISING(self):
		return self.wrapper._native_rising_falling(1)

	@property
	def HIGH(self):
		return self.wrapper._native_high_or_low(1)

	@property
	def LOW(self):
		return self.wrapper._native_high_or_low(0)

	@property
	def IN(self):
		return self.wrapper._native_in_out(1)

	@property
	def OUT(self):
		return self.wrapper._native_in_out(0)

	@property
	def PUD_DOWN(self):
		return self.wrapper._native_pull_up_down(0)

	@property
	def PUD_UP(self):
		return self.wrapper._native_pull_up_down(1)

	@property
	def PUD_OFF(self):
		return self.wrapper._native_pull_up_down(None)

def setup(id, in_or_out, pull_up_down=None, initial=0):


def cleanup:


def output:


def input:


def setmode:


def getmode:


def add_event_detect:


def remove_event_detect:


def event_detected:


def add_event_callback:


def wait_for_edge:


def gpio_function:


def setwarnings:
