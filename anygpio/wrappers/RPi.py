import importlib
from pathlib import Path

from .. import anygpio
from .. import errors

# TEMPLATE: Set to the native GPIO module name
native_gpio_name = "RPi.GPIO"


# Native GPIO module will be imported and assigned to native_gpio
try:
	# Import Native GPIO
	native_gpio = importlib.import_module(native_gpio_name)
except:
	raise errors.NoNativeGPIO("Could not import " + native_gpio_name)


class Pin(anygpio.Pin):
	"""
	Derived class for storing GPIO pin configurations and related methods

	Attributes:
		name			User defined pin name
		_id				self.id private variable
		id				Pin ID as identified by native_gpio
							Could be int (10) or could be string ("p9_10")
		number			Pin number as integer
							Used as id on systems such as RPi and Omega2
							Used in combination with header info for BeagleBone
		header			Physical header on which pin is located
							Used in systems like BeagleBone
								(id="p" + self.header + "_" + pin.number)
		is_analog		Is analog pin. False if digital, True if analog
		action			Stores the function that should be called when:
							(value() == desired_value) && GPIO._watching
		desired_value	The desired value of a pin. This should be 1
							Will be compared to value()
		supports		Stores Supports() instance for pin support configurations
		native			Native GPIO pin object if applicable
	"""

	def __init__(self, id, name=None, action=anygpio.do_nothing, **kwargs):
		"""
		Sets default values and constructs instance of Pin
		"""
		super().__init__(id, name, action, **kwargs)

		# TEMPLATE: Parse number and header (if applicable) from id by running setter
		self.id = self._id

	# This has to be here to be able so change setter method
	@property
	def id(self):
		"""
		Getter for self._id

		Pin ID as identified by native_gpio
		Could be int (01) or could be string ("p9_10")
		"""
		return self._id

	@id.setter
	def id(self, value):
		"""
		Setter function for self._id
		"""
		self._id = value

		# TEMPLATE: If id is just the pin number (int), set that here too
		self.number = value

	def destroy(self):
		"""
		Remove pin configuration through native pin object then drop pin

		Subsequently calls GPIO.drop_pin()
		"""
		# TEMPLATE: Add native pin deconfig code before drop_pin() if needed
		wrapper.drop_pin(self)


class InputPin(Pin, anygpio.InputPin):
	"""
	Derived class for storing GPIO input pin configurations and related methods
	"""

	def setup(self):
		"""
		Initialize the input pin with the native_gpio

		Initialized with pull up resistor (if available)
		"""
		# TEMPLATE: Initialize the input pin with the native_gpio
		native_gpio.setup(self.id, native_gpio.IN, pull_up_down=native_gpio.PUD_UP)

	def value(self):
		"""
		Use this to return a curated, semantic value from the pins input

		This should return (0 or 1) for LOW and HIGH respectively
		"""
		# TEMPLATE: Change this if native_gpio.input() returns 1 when button is pressed
		return int(not self.input())

	def input(self):
		"""
		Get input value of pin from the native GPIO library
		"""
		# TEMPLATE: Get input value of pin with native_gpio
		return native_gpio.input(self.id)

	def event(self, action=None, desired_value=None, both=False):
		"""
		Registers an event handler for interrupt-driven GPIO if supported

		Uses self.action as default callback
		Uses self.desired_value to determine GPIO.RISING or GPIO.FALLING
		"""

		# Don't set self.action, just use it as default
		action = action or self.action

		# Set self.desired_value if desired_value is set
		self.desired_value = desired_value or self.desired_value

		# Determine RISING, FALLING, or BOTH
		if both:
			rising_or_falling = native_gpio.BOTH
		else:
			# Determine GPIO.RISING or GPIO.FALLING
			rising_or_falling = wrapper._get_rising_falling(self.desired_value)

		# Register the event callback
		native_gpio.add_event_detect(self.id, rising_or_falling, self.action)


# TEMPLATE: Inherit from InputPin if output pins can be read
class OutputPin(anygpio.OutputPin, InputPin):
	"""
	Derived class for storing GPIO input pin configurations and related methods

	Inherits from InputPin since RPi can read output pins

	Attributes:
		initial_value	If the pin is an output, this determines initial state
							(0 or 1)
	"""

	def output(self, value):
		"""
		Output the desired value to the pin

		value should be (0 or 1).
		native_gpio.outputToPin(pin.id, GPIO._native_high_or_low(value))
		"""
		# TEMPLATE: Output the desired value to the pin
		return native_gpio.output(self.id, value)

	def setup(self):
		"""
		Initialize the output pin with the native_gpio
		"""
		# TEMPLATE: Initialize the output pin with the native_gpio
		native_gpio.setup(self.id, native_gpio.OUT, initial=wrapper._native_high_or_low(self.initial_value))


class PWMPin(anygpio.PWMPin, OutputPin):
	"""
	Derived class for storing GPIO PWM pin configurations and related methods

	Attributes:
		frequency		Array of configured pins
		duty_cycle		Stores Support() instance for system-wide support configurations
		_running		Is pwm running on this pin?
	"""

	def setup(self, frequency=None, duty_cycle=None):
		"""
		Initialize the PWM pin with the native_gpio
		"""
		# Set attributes to parameters if set
		self.frequency = frequency or self.frequency

		# TEMPLATE: Set default duty_cycle to 0 (change if necessary)
		self.duty_cycle = duty_cycle or 0

		# Run OutputPin.setup() to set up as output pin first if needed
		OutputPin.setup(self)

		# Setup the native pin
		# TEMPLATE: Native PWM pin setup
		self.native = native_gpio.PWM(self.id, self.frequency)

	def start(self, duty_cycle=None):
		"""
		Start PWM at specified duty_cycle
		"""

		# Set attributes to parameters
		self.duty_cycle = duty_cycle or self.duty_cycle

		# TEMPLATE: Start PWM on the native_gpio
		self.native.start(self.duty_cycle)

		# PWM is running
		self._running = True

	def stop(self):
		"""
		Stop PWM
		"""

		# TEMPLATE: Stop PWM on the native_gpio
		self.native.stop()

		# PWM is not running
		self._running = False

	def change_frequency(self, value):
		"""
		Update the PWM frequency
		"""

		# TEMPLATE: Run native ChangeFrequency function
		self.native.ChangeFrequency(value)

	def change_duty_cycle(self, value):
		"""
		Update the PWM duty cycle
		"""

		# TEMPLATE: Run native ChangeDutyCycle function
		self.native.ChangeDutyCycle(value)

	def destroy(self):
		"""
		Remove PWM pin configuration through native pin object then drop pin

		Stops PWM on pin, deconfigs, then calls GPIO.drop_pin()
		"""
		# TEMPLATE: If needed, do native pin deinit
		self.stop()
		wrapper.drop_pin(self)


class GPIO(anygpio.GPIO):

	def setup(self):
		"""
		Native GPIO initialization

		Can be performed after GPIO.cleanup()
		Set numbering mode, etc
		"""
		# TEMPLATE: Add GPIO initialization procedures here
		self.native.setmode(self.native.BCM)

	# This has to be here to use the overridden Pin class
	def _create_Pin_instance(*args):
		"""
		Create an instance of Pin

		Must be included in wrapper GPIO class to use overridden Pin Class
		"""
		return Pin(*args[1:])

	# This has to be here to use the overridden InputPin class
	def _create_InputPin_instance(*args):
		"""
		Create an instance of InputPin

		Must be included in wrapper GPIO class to use overridden InputPin Class
		"""
		return InputPin(*args[1:])

	# This has to be here to use the overridden OutputPin class
	def _create_OutputPin_instance(*args):
		"""
		Create an instance of OutputPin

		Must be included in wrapper GPIO class to use overridden OutputPin Class
		"""
		return OutputPin(*args[1:])

	# This has to be here to use the overridden PWMPin class
	def _create_PWMPin_instance(*args):
		"""
		Create an instance of PWMPin

		Must be included in wrapper GPIO class to use overridden PWMPin Class
		"""
		return PWMPin(*args[1:])

	# TEMPLATE: Change to LOW or HIGH of native_gpio
	def _native_high_or_low(self, value):
		"""
		Returns LOW or HIGH value from native_gpio

		Value can be (0 or 1) or (True or False)
		"""
		return native_gpio.HIGH if value else native_gpio.LOW

	# This has to be here to use the overridden InputPin class
	def _get_all_input_pins(self):
		"""
		Get all input pins from self.pins

		Must be included in wrapper GPIO class to use overridden InputPin Class
		Since OutputPins can also be read in some systems, they can inherit from InputPin
		This returns all InputPins (including OutputPins which are derived from InputPin)
		"""
		return [pin for pin in self.pins if isinstance(pin, InputPin) and not isinstance(pin, PWMPin)]

	# This has to be here to use the overridden InputPin class
	def _get_input_pins_only(self):
		"""
		Get all input pins from self.pins

		Must be included in wrapper GPIO class to use overridden InputPin Class
		Since OutputPins can also be read in some systems, they can inherit from InputPin
		This returns only InputPins
		"""
		return [pin for pin in self.pins if isinstance(pin, InputPin) and not isinstance(pin, OutputPin)]

	# TEMPLATE: Change to RISING and FALLING of native_gpio
	def _get_rising_falling(self, value):
		"""
		Returns GPIO.RISING (1) or GPIO.FALLING (0)
		"""

		return (native_gpio.RISING if value else native_gpio.FALLING)

	def cleanup(self):
		"""
		Run the native GPIO cleanup() function if available

		Should also _destroy_all_pins()
		"""
		self._destroy_all_pins()

		# TEMPLATE: run native GPIO cleanup() function if available
		native_gpio.cleanup()




# wrapper is what will be imported by __init__.py
wrapper = GPIO()


# TEMPLATE: Set GPIO Supports:
wrapper.supports.pwm = True


# Set the system to the name of the file
wrapper.system = Path(__file__).stem

# Link the native GPIO library so it can be accessed directly
wrapper.native = native_gpio

# Do native GPIO initialization
wrapper.setup()
