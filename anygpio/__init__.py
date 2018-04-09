import sys, os, signal
from importlib import import_module

from . import errors

# Set module to `this`
this = sys.modules[__name__]

# The base module path to wrappers
wrapper_path = ".wrappers."


def set_system(name):
	"""
	Imports the corresponding wrapper module

	`name` should be the same as the wrapper file's name without the extension
	"""
	try:
		#from .wrappers import RPi as SBC
		SBC = import_module(wrapper_path + name, __package__)
	except:
		# raise errors.WrapperError("Wrapper `" + sbc_name + "` could not be imported")
		raise

	# Set GPIO to the wrapper returned from the SBC file
	this.GPIO = SBC.wrapper

	# Return GPIO so it can be set to the result of this command
	return this.GPIO


# Set the system to RPi to default for compatibility purposes
# Should probably be removed for performance
set_system("RPi")


class ExitHandler:
	"""
	Handles exits for anygpio by calling cleanup()
	"""
	exiting = False

	# Store original sigint handler to prevent exit if _watching
	original_handler = signal.getsignal(signal.SIGINT)

	def register_exit_handlers(self):
		"""
		Clean up GPIO data on SIGTERM or SIGINT
		"""
		signal.signal(signal.SIGTERM, self.exit)
		signal.signal(signal.SIGINT, self.exit)


	# Use *_ to "ignore" all arguments
	def exit(self, *_):
		"""
		Contains tasks to be completed just before exiting

		Also currently contains the only stop watching check, which
			should be its own method
		"""
		# If watch() is running, just stop_watching()
		if (this.GPIO._watching):
			this.GPIO.stop_watching()
			signal.signal(signal.SIGINT, self.original_handler)
			self.register_exit_handlers()
			return

		# If not already exiting
		if not self.exiting:
			# Set exiting flag to avoid multiple calls to this function
			self.exiting = True

			print("Exiting cleanly...")
			this.GPIO.stop_watching()
			# Run cleanup()
			this.GPIO.cleanup()
			sys.exit(0)

exit_handler = ExitHandler()

exit_handler.register_exit_handlers()
