import importlib

from .. import anygpio
from .. import errors

# TEMPLATE: Set to the native GPIO module name
native_gpio_name = "onionGpio"


# Native GPIO module will be imported and assigned to native_gpio
try:
    # Import Native GPIO
    native_gpio = importlib.import_module(native_gpio_name)
except:
    raise errors.NoNativeGPIO("Could not import " + native_gpio_name)

# Generic Pin class
class Pin(anygpio.Pin):

    @property
    def id(self):
        return self.number

    @id.setter
    def id(self, value):
        # Set self._id
        self.number = value

    def value(self):
        """
        Use this to return a curated, semantic value from the pins input

        For instance, on RPi, when a button is pressed, input() returns False
        This function should make it return True instead
        """
        return self.input()

    def input(self):
        # Get input value of pin from the native GPIO library
            return self.native.getValue()

    def output(self, value):
        # Outputs the desired value to the pin
        # Value is 1 (HIGH) or 0 (LOW)
        if (self.is_output):
            return self.native.setValue(value)
        else:
            raise errors.WrongPinType("Pin is set to input")

    def setup(self):
        # Set up the pin using native_gpio
        # TODO: test this for pull_up_down
        self.native = native_gpio.OnionGpio(self.id)
        if self.is_output:
            self.native.setOutputDirection(self.initial_value)
        else:
            self.native.setInputDirection()

    def destroy(self):
        self.native._freeGpio()
        wrapper.drop_pin(self)

# Generic module class
class GPIO(anygpio.GPIO):
    # This has to be here to use the derived Pin class for initialization
    def setup_pin(self, number, name=None, action=anygpio.do_nothing, is_output=False, initial_value=0):
        # Use this to initialize a pin
        # Require the system to be set
        self._require_system_set()
        pin = Pin(name, number, action, is_output, initial_value)
        pin.setup()
        self._add_pin(pin)

    def cleanup(self):
        self._destroy_all_pins()

# wrapper is what will be imported by __init__.py
wrapper = GPIO()

# Set the system to the name of the file
wrapper.system = "Omega2"

# Link the native GPIO library so it can be accessed directly
wrapper.native = native_gpio
