* Dynamic ImportError module names
* Destroy if pin already exists in setup_pin
* Better differentiation between SystemNotSet and NotSupportedOnSystem
* supports.read_output_pin
* Conversion function from (0 or 1) / (True or False) to (GPIO.HIGH or GPIO.LOW)
* BeagleBone uses weird pin numbering, ensure that this works (Add header attribute and getter function? Or generic converter using a dict in available_pins?)
  - p8_1, p9_11
* supports.available_pins or ground_pins
* Packagify wrappers?
* GPIO.destroy() on exit

* Pull up and pull down resistor setting
* Format and improve README

Wrappers for:
  - BeagleBone
  - C.H.I.P.
  - Orange Pi
  - Nano Pi
  - Pine A64
  - Minnow Board
  - micro:bit
  - Parallela
  - Banana Pi
  - ODroid
