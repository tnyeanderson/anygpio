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
		native_gpio.setup(self.id, native_gpio.IN, pull_up_down=wrapper._native_pull_up_down(self.pull_up_down))

	def value(self):
		"""
		Use this to return a curated, semantic value from the pins input for watch()

		This should return (0 or 1) for INACTIVE and ACTIVE respectively
		If there is a pull up resistor this should return 0 for HIGH and 1 for LOW
		"""
		# TEMPLATE: Change this if native_gpio.input() returns 1 when button is pressed
		return int(not self.input() if self.pull_up_down else self.input())

	def input(self):
		"""
		Get input value of pin from the native GPIO library
		"""
		# TEMPLATE: Get input value of pin with native_gpio
		return native_gpio.input(self.id)

	def _add_event(self, rising_or_falling, action, bounce):
		"""
		Register an event callback with the native_gpio
		"""

		# TEMPLATE: Set the default bouncetime in milliseconds (300)
		bounce = bounce or 300

		# TEMPLATE: Call the native add_event_detect function
		native_gpio.add_event_detect(self.id, rising_or_falling, action, bouncetime=bounce)

	def _remove_event(self):
		"""
		Call the native remove_event_detect() method
		"""

		# TEMPLATE: Call the native remove_event_detect() method
		native_gpio.remove_event_detect(self.id)

	def _native_rising_falling(*args):
		"""
		Call the wrapper._native_rising_falling() method

		This has to be here to have access to the wrapper variable
		"""

		return wrapper._native_rising_falling(*args[1:])


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
	def _create_Pin_instance(*args, **kwargs):
		"""
		Create an instance of Pin
		"""
		return Pin(*args[1:], **kwargs)

	# This has to be here to use the overridden InputPin class
	def _create_InputPin_instance(*args, **kwargs):
		"""
		Create an instance of InputPin
		"""
		return InputPin(*args[1:], **kwargs)

	# This has to be here to use the overridden InputPin class
	def _create_OutputPin_instance(*args, **kwargs):
		"""
		Create an instance of OutputPin
		"""
		return OutputPin(*args[1:], **kwargs)

	# This has to be here to use the overridden InputPin class
	def _create_PWMPin_instance(*args, **kwargs):
		"""
		Create an instance of PWMPin
		"""
		return PWMPin(*args[1:], **kwargs)

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
		return [pin for pin in self.pins.values() if isinstance(pin, InputPin) and not isinstance(pin, PWMPin)]

	# This has to be here to use the overridden InputPin class
	def _get_input_pins_only(self):
		"""
		Get all input pins from self.pins

		Must be included in wrapper GPIO class to use overridden InputPin Class
		Since OutputPins can also be read in some systems, they can inherit from InputPin
		This returns only InputPins
		"""
		return [pin for pin in self.pins.values() if isinstance(pin, InputPin) and not isinstance(pin, OutputPin)]

	def _native_pull_up_down(self, value):
		"""
		Returns GPIO.PUD_UP (1) or GPIO.PUD_DOWN (0) or None (None)
		"""

		self.supports.require('pull_up_down')

		if value == 0:
			# Pull down resistor
			return native_gpio.PUD_DOWN

		elif value == 1:
			# Pull up resistor
			return native_gpio.PUD_UP

		else:
			# (None) No pull up or pull down resistor (floating)
			return native_gpio.PUD_OFF

	# TEMPLATE: Change to RISING and FALLING of native_gpio
	def _native_rising_falling(self, value):
		"""
		Returns GPIO.RISING (1) or GPIO.FALLING (0)
		"""

		self.supports.require('events')

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
wrapper.supports.pull_up_down = True
wrapper.supports.events = True


# Set the system to the name of the file
wrapper.system = Path(__file__).stem

# Link the native GPIO library so it can be accessed directly
wrapper.native = native_gpio

# Do native GPIO initialization
wrapper.setup()
