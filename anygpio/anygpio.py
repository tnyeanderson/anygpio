import sys
import os
from . import errors

# Requrire sudo
if os.getuid() != 0:
    print("Requires sudo privileges")


def do_nothing():
    pass



# Generic Supports class
class Supports:
    def __init__(self):
        pass

# Generic Pin class
class Pin:
    def __init__(self, name=None, number=None, action=do_nothing, is_output=False):
        self.name = name
        self.number = number
        self.is_analog = False
        self.is_output = is_output
        self.action = action
        self.desired_value = True

    def value(self):
        """
        Use this to return a curated, semantic value from the pins input

        For instance, on RPi, when a button is pressed, input() returns False
        This function should make it return True instead
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
        # native_gpio.setup(self.number, GPIO.OUT if self.is_output else GPIO.IN)


# Generic module class
class AnyGPIO:
    def __init__(self):
        # Empty pin array
        self.pins = []
        self.supports = Supports()
        self.system = None

    def setup_pin(self):
        # Use this to initialize a pin

        raise errors.SystemNotSet("Please set your system first")
        self._add_pin(pin)

    def _add_pin(self, pin):
        self.pins.append(pin)

    def drop_pin(self ):
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
