import sys

# Set module to `this`
this = sys.modules[__name__]

# Change this to your SBC's file
from .wrappers import RPi as SBC

# Set GPIO to the wrapper returned from the SBC file
this.GPIO = SBC.wrapper
