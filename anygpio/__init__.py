import sys
from importlib import import_module

from . import errors

# Set module to `this`
this = sys.modules[__name__]

# Change this to your SBC's file
sbc_name = "RPi"

try:
    SBC = import_module("anygpio.wrappers." + sbc_name)
except:
    raise errors.WrapperError("Wrapper `" + sbc_name + "` could not be imported")

# Set GPIO to the wrapper returned from the SBC file
this.GPIO = SBC.wrapper
