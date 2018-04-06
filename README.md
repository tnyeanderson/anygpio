# Cross-Platform GPIO library for Single-Board Computers

*This project is a work in progress, changes may be made at any time that may not be backwards compatible. Submit a pull request to help make this not a WIP!*

This goal of this project is to create a "universal"
language for simple GPIO functions on Single-Board Computers (SBCs). Currently, this involves simple pin initialization, reading input (HIGH or LOW), and outputting to the pin (HIGH or LOW). PWM is also supported when available. More functionality may be added later (such as event-driven GPIO).

This project is designed to be modular and accessible. It provides access to any native GPIO objects so you will never lose functionality using this library as long as your SBC is supported (check the `anygpio/wrappers` folder for your SBC).

## Currently supported:

* Raspberry Pi (RPi.GPIO)
* Omega2 (onionGpio) [Not tested]
* C.H.I.P (CHIP_IO) [Not tested]
* BeagleBone (Adafruit_BBIO) [Not tested]

*If you don't see your favorite SBC on the list, submit a pull request!*

Just use `anygpio/wrappers/RPi.py` as a template. All you need to change is a few lines to contribute!

## Important Notes

`(0 or 1)` should be used as GPIO.LOW and GPIO.HIGH respectively

Currently, this library requires you to change `__init__.py` to import your SBC's corresponding wrapper file. This is not ideal. There are plans in the future to create a separate python package that will be used to identify the current SBC in use, and this library will use that to import the corresponding wrapper file.

---

# Getting Started

*To install:*
```
git clone https://github.com/tnyeanderson/anygpio
cd anygpio
sudo pip3 install --upgrade .
```

Then:

```
from anygpio import GPIO
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
GPIO.setup_pin(18, "MY_OUTPUTTER", is_output=True, initial_value=1)
```

---

## Using pins

Return a `pin` from the `pin` array
```
# Searches by `pin.number` (int)
GPIO.pin(18)

# Searches by `pin.name` (string)
GPIO.pin("MY_BUTTON")
```

In `GPIO.pin(id)`, `id` is what will be passed to the Native GPIO library to identify the pin.

In RPi, this is the same as `pin.number` but on other systems (like BeagleBone) it is a combination of `pin.number` and `pin.header` (`'p9_10'`) or something else entirely (C.H.I.P)!

If searching for an `id` that is a string (like on CHIP or BeagleBone), set `id` explicitly
```
GPIO.pin(id="p9_10")
```

### Destroy a pin
```
GPIO.pin(18).destroy()
```

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

Explicit setting of RISING/FALLING coming soon!

```
GPIO.pin(18).event()

# Use a different callback
GPIO.pin(18).event(action=my_different_callback)

# Set a different bounce time in milliseconds (Default: 300ms)
GPIO.pin(18).event(bounce=1000)

# Watch for both RISING and FALLING events
GPIO.pin(18).event(both=True)

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
