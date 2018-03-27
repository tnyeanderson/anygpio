import sys
import os
from . import errors

# Requrire sudo
if os.getuid() != 0:
    print("Requires sudo privileges")


def do_nothing():
    print("Debug: do_nothing occurred")
    pass



# Generic Supports class
class Supports:
    def __init__(self):
        pass

# Generic Pin class
class Pin:
    def __init__(self, number, name=None, action=do_nothing, is_output=False):
        self.name = name
        self.number = number
        self.is_analog = False
        self.is_output = is_output
        self.action = action
        self.desired_value = True
        self.supports = Supports()
        # Stores native GPIO pin objects
        self.native = None

    def value(self):
        """
        Use this to return a curated, semantic value from the pins input

        For instance, on RPi, when a button is pressed, input() returns 0
        This function should make it return 1 instead
        """
        return self.input()

    def input(self):
        # Get input value of pin from the native GPIO library

        if (self.is_output):
            raise errors.WrongPinType("Pin is set to output")
        else:
            raise errors.SystemNotSet("Please set your system first")
            # return native_gpio.getPinInput(pin.number)

    def output(self, value):
        # Outputs the desired value to the pin
        if (self.is_output):
            raise errors.SystemNotSet("Please set your system first")
            # return native_gpio.outputToPin(pin.number, value)
        else:
            raise errors.WrongPinType("Pin is set to input")

    def setup(self):
        # Use this to initialize the pin with the native_gpio

        raise errors.SystemNotSet("Please set your system first")
        # native_gpio.setup(self.number, native_gpio.OUT if self.is_output else native_gpio.IN)

    def destroy(self):
        raise errors.SystemNotSet("Please set your system first")


# Generic module class
class GPIO:
    def __init__(self):
        # Empty pin array
        self.pins = []
        self.supports = Supports()
        self.system = None
        self.native = None

    def _require_system_set(self):
        if not self.system:
            raise errors.SystemNotSet("Please set your system first")

    def setup_pin(self, name, number, action=do_nothing, is_output=False):
        # Use this to initialize a pin
        self._require_system_set()
        pin = Pin(name, number, action, is_output)
        pin.setup()
        self._add_pin(pin)

    def _add_pin(self, pin):
        self.pins.append(pin)

    def drop_pin(self, pin):
        # Use this to remove a pin configuration
        self._require_system_set()
        self._remove_pin(pin)

    def _remove_pin(self, pin):
        self.pins.remove(pin)

    def pin(self, pin_id):
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

    def destroy():
        # Run the native GPIO cleanup() function if available
        self._require_system_set()

    def watch(self):
        # Watch all pins for their desired_value, and execute pin.action()
        # Stops only with a KeyboardInterrupt or by killing the process!
        while True:
            for pin in self.pins:
                if pin.value() == pin.desired_value:
                    pin.action()
