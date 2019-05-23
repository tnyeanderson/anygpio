# Cross-Platform GPIO library for Single-Board Computers

*This project is a work in progress, changes may be made at any time that may not be backwards compatible. Submit a pull request to help make this not a WIP!*

This goal of this project is to create a "universal"
language for simple GPIO functions on Single-Board Computers (SBCs). Currently, this involves simple pin initialization, reading input (HIGH or LOW), and outputting to the pin (HIGH or LOW). PWM and event-driven GPIO are also supported, when available.

This project is designed to be modular and accessible. It provides access to any native GPIO objects so you will never lose functionality using this library as long as your SBC is supported (check the `anygpio/wrappers` folder for your SBC).

## Currently supported:

* Raspberry Pi ([RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO))
* Omega2 ([onionGpio](https://docs.onion.io/omega2-docs/gpio-python-module.html)) `[Not tested]`
* C.H.I.P ([CHIP_IO](https://github.com/xtacocorex/CHIP_IO)) `[Not tested]`
* BeagleBone ([Adafruit_BBIO](https://github.com/adafruit/adafruit-beaglebone-io-python)) `[Not tested]`
* OrangePi ([OPi.GPIO](https://github.com/rm-hull/OPi.GPIO)) `[Not tested]`
	- See the [OPi Documentation](https://opi-gpio.readthedocs.io/en/latest/api-documentation.html) about pull_up_down support and bouncetime
- BananaPi ([BPI-SINOVOIP/RPi.GPIO](https://github.com/BPI-SINOVOIP/RPi.GPIO)) `[Not tested]`
- NanoPi ([RPi.GPIO_NP](https://github.com/auto3000/RPi.GPIO_NP)) `[Not tested]`
- Pine A64 ([RPi.GPIO-PineA64](https://github.com/swkim01/RPi.GPIO-PineA64)) `[Not tested]`

*If you don't see your favorite SBC on the list, submit a pull request!*

Just use `anygpio/wrappers/RPi.py` as a template. All you need to change is a few lines to contribute!

## Important Notes

`(0 or 1)` should be used as GPIO.LOW and GPIO.HIGH respectively

Currently, this library requires you to set your system (See **Getting Started**) to import your SBC's corresponding wrapper file. This is not ideal. There are plans in the future to create a separate python package that will be used to identify the current SBC in use, and this library will use that to import the corresponding wrapper file.

---

# Getting Started

*To install:*
```
git clone https://github.com/tnyeanderson/anygpio
cd anygpio
sudo pip3 install --upgrade .
```

*Then:*

To import the default wrapper (RPi.GPIO):
```
from anygpio import GPIO
```

Or, to set your system manually:
```
import anygpio

# Use the file name in wrappers without the extension.
# For example, CHIP
GPIO = anygpio.set_system("CHIP")
```

---

## Pin initialization

### Input pins

Pins are initialized to inputs by default, with a pull up resistor. The reason being that many input pins are buttons connected to ground by default.
```
GPIO.setup_pin(18, "MY_BUTTON", my_button_pressed_function)
```

This will set up a button on pin with `id=18`, connected to ground with a *pull up* resistor.
```
GPIO.setup_pin(18)
```

### Output pins

Default initial value is always `0` (LOW) unless set here
```
GPIO.setup_pin(18, "MY_OUTPUTTER", out=True, initial_value=1)
```

---

## Using pins

Pins are stored in the dictionary `GPIO.pins`. The key for each pin is its `id`.

Returns a `pin` from the `pin` array. If the argument is a key in GPIO.pins, that pin is returned. Otherwise it searches by `pin.number` (if int) or `pin.name` (if string)
```
# Returns the pin with id=18 by key lookup in GPIO.pins
GPIO.pin(18)

# This is the same as accessing the pin directly
GPIO.pins[18]

# If pin with id 18 doesn't exist...

# Searches by `pin.number` (int)
GPIO.pin(18)

# Searches by `pin.name` (string)
GPIO.pin("MY_BUTTON")
```

`id` is what will be passed to the Native GPIO library to identify the pin.

In RPi, this is the same as `pin.number` but on other systems (like BeagleBone) it is a combination of `pin.number` and `pin.header` (`'p9_10'`) or something else entirely (C.H.I.P)!

---

### Reading input pins

Actual input value:
```
# Pull up resistor by default!
# returns: 1
print(GPIO.pin(18).input())
```

Curated input value. Buttons should be `1` (True) when pressed, and `0` (False) when not pressed:
```
# returns: 0
print(GPIO.pin(18).value())
```

---

### Watch pins (infinite loop)

Watch all InputPins for their `desired_value` and run their respective `action` methods if they match

If pin 18 is hooked up to a button and the button is pressed, `my_button_pressed_function()` will be run

Stops only with a `KeyboardInterrupt`, changing `_watching` to `False`,
	or by killing the process!

Can also call `stop_watching()` from signal triggered process. For an example, see `ExitHandler.exit()`
```
GPIO.watch()

# Change the interval (in seconds) between each check (Default is 0.15)
GPIO.watch(0.2)

# Watch output pins also (if supported by system)
GPIO.watch(watch_outputs=True)
```

---

### Interrupt Driven GPIO

Register an event callback for the given pin, using `pin.action` as default callback

If pin 18 is hooked up to a button and the button is pressed, `my_button_pressed_function()` will be run.

RISING or FALLING is determined by pull up or pull down resistor by default


```
GPIO.pin(18).event()

# Use a different callback
GPIO.pin(18).event(action=my_different_callback)

# Set a different bounce time in milliseconds (Default: 300ms)
GPIO.pin(18).event(bounce=1000)

# Watch for both RISING and FALLING events
GPIO.pin(18).event(both=True)

# To set FALLING or RISING explicitly
# Use (0 or 1) for FALLING and RISING respectively
GPIO.pin(18).event(rising_falling=1)


# Deregister an event callback
GPIO.pin(18).remove_event()
```

---

### Output to pins

Output HIGH to a pin
```
GPIO.pin(18).output(1)
```

Output LOW to a pin
```
GPIO.pin(18).output(0)
```


---

### PWM Pins

Set up PWM pin
```
GPIO.PWM(18, 1000, name="MY_PWM")
```

---

Start PWM on a pin
```
GPIO.pin(18).start(50)
```

---

Stop PWM on a pin
```
GPIO.pin(18).stop()
```

---

Change Duty Cycle on PWM pin
```
GPIO.pin(18).change_duty_cycle(75)
```

---

## Cleaning up

Destroy a pin
```
GPIO.pin(18).destroy()
```

Run native GPIO cleanup functions
```
GPIO.cleanup()
```

After cleaning up, if you need to start using GPIO again from within your program, first re-initialize the GPIO
```
GPIO.setup()
```

---

*Better docs, more wrappers, and more features to come!*
