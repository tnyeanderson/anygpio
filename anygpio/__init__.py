import sys, os, signal
from importlib import import_module

from . import errors

# Set module to `this`
this = sys.modules[__name__]

# The base module path to wrappers
wrapper_path = ".wrappers."

# Change this to your SBC's file
sbc_name = "RPi"

try:
    #from .wrappers import RPi as SBC
    SBC = import_module(wrapper_path + sbc_name, __package__)
except:
    # raise errors.WrapperError("Wrapper `" + sbc_name + "` could not be imported")
    raise


# Set GPIO to the wrapper returned from the SBC file
this.GPIO = SBC.wrapper

class ExitHandler:
    # Handles exits for anygpio by calling cleanup()
    exiting = False

    # Use *_ to "ignore" all arguments
    def exit(self, *_):
        # Set exiting flag to avoid multiple calls to this function
        self.exiting = True

        # If not already exiting
        if self.exiting:
            print("Exiting!")
            this.GPIO.stop_watching()
            # Run cleanup()
            this.GPIO.cleanup()
            # os._exit(0)

exit_handler = ExitHandler()

# Clean up on KILL signal
signal.signal(signal.SIGTERM, exit_handler.exit)
signal.signal(signal.SIGINT, exit_handler.exit)
