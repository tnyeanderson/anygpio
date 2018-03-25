import sys

# Set module to `this`
this = sys.modules[__name__]

from .wrappers import RPi

this = RPi.GPIO()
