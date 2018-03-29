import importlib

from .. import anygpio
from .. import errors

# TEMPLATE: Set to the native GPIO module name
native_gpio_name = "RPi.GPIO"


# Native GPIO module will be imported and assigned to native_gpio
try:
    # Import Native GPIO
    native_gpio = importlib.import_module(native_gpio_name)
except:
    raise errors.NoNativeGPIO("Could not import " + native_gpio_name)

# TEMPLATE: to the correct native setmode() function if required, or delete line
# Always use BCM Mode
native_gpio.setmode(native_gpio.BCM)

# Derived Pin class
# TEMPLATE: Each method in the Pin class must be changed to use the native_gpio module
class Pin(anygpio.Pin):

    # TEMPLATE: Change to what the native_gpio will accept as pin identifier
    @property
    def id(self):
        return self.number

    def value(self):
        """
        Use this to return a curated, semantic value from the pins input

        For instance, on RPi, when a button is pressed, input() returns 0
        This function should make it return 1 instead for semantic reasons
        """
        return int(not self.input())

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
            return native_gpio.output(self.id, value)
        else:
            raise errors.WrongPinType("Pin is set to input")

    def setup(self):
        # Set up the pin using native_gpio
        # TODO: test this for pull_up_down
        if self.is_output:
            native_gpio.setup(self.id, native_gpio.OUT, initial=self.initial_value)
        else:
            native_gpio.setup(self.id, native_gpio.IN, pull_up_down=(None if self.is_output else native_gpio.PUD_UP))

class GPIO(anygpio.GPIO):
    # TEMPLATE: Change argument initial_value to the native_gpio.LOW value if needed
    def setup_pin(self, name, number, action=anygpio.do_nothing, is_output=False, initial_value=0):
        # Use this to initialize a pin
        # Require the system to be set
        self._require_system_set()
        # Create a pin
        pin = Pin(number, name, action, is_output, initial_value)
        pin.setup()
        self._add_pin(pin)

    # TEMPLATE: Change to LOW or HIGH of native_gpio or delete if not needed
    def _native_high_or_low(self, value):
        return native_gpio.HIGH if value else native_gpio.LOW

    # TEMPLATE: run native GPIO cleanup() function if available
    def cleanup():
        native_gpio.cleanup()

# wrapper is what will be imported by __init__.py
wrapper = GPIO()

# TEMPLATE: Set the system to the name of the file
wrapper.system = "RPi"

# Link the native GPIO library so it can be accessed directly
wrapper.native = native_gpio
