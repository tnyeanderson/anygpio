from .. import anygpio

try:
    # Import GPIO
    import RPi.GPIO as GPIO
except ImportError:
    raise ImportError("No module RPi.GPIO")


# Generic Pin class
class Pin(anygpio.Pin):
    def value(self):
        """
        Use this to return a curated, semantic value from the pins input

        For instance, on RPi, when a button is pressed, input() returns False
        This function should make it return True instead
        """
        return not self.input()

    def input(self):
        # Get input value of pin from the native GPIO library

        if (self.is_output):
            raise errors.WrongPinType("Pin is set to output")
        else:
            return native_gpio.input(pin.number)

    def output(self, value):
        # Outputs the desired value to the pin
        # Value is True (HIGH) or False (LOW)
        if (self.is_output):
            return native_gpio.output(self.number, value)
        else:
            raise errors.WrongPinType("Pin is set to input")

    def setup(self):
        # Set up the pin using native_gpio
        # TODO: test this for pull_up_down
        native_gpio.setup(self.number, GPIO.OUT if self.is_output else GPIO.IN, pull_up_down=(None if self.is_output else native_gpio.PUD_UP))


# Generic module class
class GPIO(anygpio.AnyGPIO):
    def setup_pin(self, name, number, action=anygpio.do_nothing, is_output=False):
        # Use this to initialize a pin
        pin = Pin(name, number, action, is_output)
        pin.setup()
        self._add_pin(pin)

    def _add_pin(self, pin):
        self.pins.append(pin)

    def drop_pin(self):
        # Use this to remove a pin configuration
        raise errors.SystemNotSet("Please set your system first")

    def _remove_pin(self, pin):
        self.pins.remove(pin)

    def get_pin(self, pin_id):
        # Find a pin in the pins array
        # pin_id could be pin.name or pin.number

        if isinstance(pin_id, int):
            # If pin_id is pin.number
            for pin in self.pins:
                if pin_id == pin.number:
                    return pin
        else:
            # If pin_id is pin.name
            for pin in self.pins:
                if pin_id == pin.name:
                    return pin

        # If pin is not found
        return False

    def watch(self):
        # Watch all pins for their desired_value, and execute pin.action()
        for pin in self.pins:
            if pin.value() == pin.desired_value:
                pin.action()
