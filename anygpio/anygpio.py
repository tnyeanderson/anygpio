import sys
import os
import .errors

echo __name__

# Set module to `this`
this = sys.modules[__name__]

echo this

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
    def __init__(self):
        self.name = None
        self.number = None
        self.is_analog = False
        self.is_output = False
        self.action = do_nothing
        self.desired_value = True

    def value():
        """
        Use this to return a curated, semantic value from the pins input

        For instance, on RPi, when a button is pressed, input() returns False
        This function should make it return True instead
        """
        return self.input()

    def input():
        # Get input value of pin from the native GPIO library

        if (pin.is_output):
            raise errors.WrongPinType("Pin is set to output")
        else
            raise errors.SystemNotSet("Please set your system first")
            # return native_gpio.getPinInput(pin.number)

    def output(value):
        # Outputs the desired value to the pin
        if (pin.is_output):
            raise errors.SystemNotSet("Please set your system first")
            # return native_gpio.outputToPin(pin.number, value)
        else
            raise errors.WrongPinType("Pin is set to input")

# Generic module class
class AnyGPIO:
    def __init__(self):
        # Empty pin array
        self.pins = []
        self.supports = Supports()
        self.system = None

    def setup_pin():
        # Use this to initialize a pin

        raise errors.SystemNotSet("Please set your system first")

    def _add_pin(pin):
        self.pins.append(pin)

    def drop_pin():
        # Use this to remove a pin configuration
        raise errors.SystemNotSet("Please set your system first")

    def _remove_pin(pin):
        self.pins.remove(pin)

    def get_pin(pin_id):
        # Find a pin in the pins array
        # pin_id could be pin.name or pin.number

        if isinstance(pin_id, int):
            # If pin_id is pin.number
            for pin in self.pins:
                if pin_id == pin.number:
                    return pin
        else
            # If pin_id is pin.name
            for pin in self.pins:
                if pin_id == pin.name:
                    return pin

        # If pin is not found
        return False

    def watch():
        # Watch all pins for their desired_value, and execute pin.action()
        for pin in self.pins:
            if pin.value() == pin.desired_value:
                pin.action()
