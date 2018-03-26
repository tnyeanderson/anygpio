from .. import anygpio

# Not tested on hardware yet

try:
    # Import GPIO
    import onionGpio as native_gpio
except ImportError:
    raise ImportError("No module onionGpio")

# Always use BCM Mode
native_gpio.setmode(native_gpio.BCM)

# Generic Pin class
class Pin(anygpio.Pin):
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
        self.native = native_gpio.OnionGpio(self.number)
        if self.is_output:
            self.native.setOutputDirection()
        else:
            self.native.setInputDirection()

# Generic module class
class GPIO(anygpio.GPIO):
    # This has to be here to use the derived Pin class for initialization
    def setup_pin(self, name, number, action=anygpio.do_nothing, is_output=False):
        # Use this to initialize a pin
        pin = Pin(name, number, action, is_output)
        pin.setup()
        self._add_pin(pin)

# wrapper is what will be imported by __init__.py
wrapper = GPIO()

# Set the system to the name of the file
wrapper.system = "Omega2"

# Link the native GPIO library so it can be accessed directly
wrapper.native = native_gpio
