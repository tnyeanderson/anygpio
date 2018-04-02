# Cross-Platform GPIO library for Single-Board Computers

*This project is a work in progress, changes may be made at any time that may not be backwards compatible. Submit a pull request to help make this not a WIP!*

This goal of this project is to create a "universal"
language for simple GPIO functions on Single-Board Computers (SBCs). Currently, this involves simple pin initialization, reading input (HIGH or LOW), and outputting to the pin (HIGH or LOW). More functionality may be added later (such as PWM).

This project is designed to be modular and accessible. It provides access to any native GPIO objects so you will never lose functionality using this library as long as your SBC is supported (check the `anygpio/wrappers` folder for your SBC).

*If you don't see your favorite SBC on the list, submit a pull request!*

Just use `anygpio/wrappers/RPi.py` as a template. All you need to change is a few lines to contribute!

Currently, this library requires you to change `__init__.py` to import your SBC's corresponding wrapper file. This is not ideal. There are plans in the future to create a separate python package that will be used to identify the current SBC in use, and this library will use that to import the corresponding wrapper file.

---

# Getting Started

```
from anygpio import GPIO
```



Pins are initialized to inputs by default
```
GPIO.setup_pin(18, "MY_BUTTON", my_button_pressed_function)
```
or, more simply:
```
GPIO.setup_pin(18)
```

---

Return a `pin` from the `pin` array
```
GPIO.pin(18)
GPIO.pin("MY_BUTTON")
```

---

In `GPIO.pin()`, `id` is what will be passed to the Native GPIO library to identify the pin.

In RPi, this is just `pin.number` but on other systems (like BeagleBone) it is a combination of `pin.number` and `pin.header` (`'p9_10'`) or something else entirely (C.H.I.P)!
```
GPIO.pin(id=18)
```

---

Curated input value. Buttons should be `1` (True) when pressed, and `0` (False) when not pressed
```
# returns: 0
print(GPIO.pin(18).value())
```

---

Actual input value
```
# returns: 1
print(GPIO.pin(18).input())
```

---

Watch all the pins for their `desired_value` and run their respective `action` methods if they match

If pin 18 is hooked up to a button and the button is pressed, `my_button_pressed_function()` will be run

Stops only with a `KeyboardInterrupt`, changing `_watching` to `False`,
	or by killing the process!

Can also call `stop_watching()` from signal triggered process. For an example, see `ExitHandler.exit()`
```
GPIO.watch()
```

---

Set up output pin
Default initial value is always `0` (LOW) unless set here
```
GPIO.setup_pin(18, "MY_OUTPUTTER", is_output=True, initial_value=1)
```

---

Output LOW to a pin
```
GPIO.pin(18).output(0)
```

---

Output HIGH to a pin
```
GPIO.pin(18).output(1)
```

---

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


Run native GPIO cleanup functions
```
GPIO.destroy()
```

---

*Better docs, more wrappers, and more features to come!*
