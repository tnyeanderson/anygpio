import sys, os
import atexit, signal
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

# Clean up on "clean" exit
atexit.register(this.GPIO.cleanup)

# Clean up on KILL signal
signal.signal(signal.SIGTERM, this.GPIO.cleanup)
signal.signal(signal.SIGINT, this.GPIO.cleanup)
