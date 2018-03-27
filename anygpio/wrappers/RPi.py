import importlib

from .. import anygpio
from .. import errors

# TEMPLATE: Set to the native GPIO module name
native_gpio_name = "RPi.GPIO"


# Native GPIO module will be imported and assigned to native_gpio
try:
    # Import Native GPIO
    native_gpio = importlib.import_module(native_gpio_name)
except ImportError:
    raise errors.NoNativeGPIO("Could not import " + native_gpio_name)

# TEMPLATE: to the correct native setmode() function if required, or delete line
# Always use BCM Mode
native_gpio.setmode(native_gpio.BCM)

# Derived Pin class
# TEMPLATE: Each method in this class must be changed to use the native_gpio module
class Pin(anygpio.Pin):
    def value(self):
        """
        Use this to return a curated, semantic value from the pins input

        For instance, on RPi, when a button is pressed, input() returns 0
        This function should make it return 1 instead for semantic reasons
        """
        return 0 if self.input() else 1

    def input(self):
        # Get input value of pin from the native GPIO library

        if (self.is_output):
            raise errors.WrongPinType("Pin is set to output")
        else:
            return native_gpio.input(self.number)

    def output(self, value):
        # Outputs the desired value to the pin
        # Value is 1 (HIGH) or 0 (LOW)
        if (self.is_output):
            return native_gpio.output(self.number, value)
        else:
            raise errors.WrongPinType("Pin is set to input")

    def setup(self):
        # Set up the pin using native_gpio
        # TODO: test this for pull_up_down
        if self.is_output:
            native_gpio.setup(self.number, native_gpio.OUT)
        else:
            native_gpio.setup(self.number, native_gpio.IN, pull_up_down=(None if self.is_output else native_gpio.PUD_UP))

class GPIO(anygpio.GPIO):
    # This has to be here to use the derived Pin class for initialization
    def setup_pin(self, name, number, action=anygpio.do_nothing, is_output=False):
        # Use this to initialize a pin
        self._require_system_set()
        pin = Pin(name, number, action, is_output)
        pin.setup()
        self._add_pin(pin)

# wrapper is what will be imported by __init__.py
wrapper = GPIO()

# TEMPLATE: Set the system to the name of the file
wrapper.system = "RPi"

# Link the native GPIO library so it can be accessed directly
wrapper.native = native_gpio
