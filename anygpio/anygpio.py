import sys, os, time

from . import errors

# Require sudo
if os.getuid() != 0:
	print("Requires sudo privileges")


def do_nothing():
	"""
	Don't do anything. Used as default pin.action
	"""
	pass



# Generic Supports class
class Supports:
	"""
	Base class for storing features supported on a given system

	In the future, this will contain pwm, pull_up_down, etc
	"""
	def __init__(self):
		pass

# Generic Pin class
class Pin:
	"""
	Base class for storing GPIO pin configurations and related methods

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
		is_output		Is output pin. False if input, True if output
							Pins are set to inputs by default.
		action			Stores the function that should be called when:
							(value() == desired_value) && GPIO._watching
		desired_value	The desired value of a pin. This should be 1
							Will be compared to value()
		initial_value	If the pin is an output, this determines initial state
							(0 or 1)
		supports		Stores Supports() instance for pin support configurations
		native			Native GPIO pin object if applicable
	"""

	def __init__(self, number, name=None, action=do_nothing, header=None, is_output=False, initial_value=None, id=None):
		"""
		Sets default values and constructs instance of Pin
		"""
		self.name = name
		self._id = None
		self.id = id
		self.number = number
		self.header = header
		self.is_analog = False
		self.is_output = is_output
		self.action = action
		self.desired_value = 1
		self.initial_value = initial_value
		self.supports = Supports()
		self.native = None

	def value(self):
		"""
		Use this to return a curated, semantic value from the pins input

		For instance, on RPi, when a button is pressed, self.input() returns 0
		This function should make it return 1 instead
		"""
		return self.input()

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

	def input(self):
		"""
		Get input value of pin from the native GPIO library
		"""
		if (self.is_output):
			raise errors.WrongPinType("Pin is set to output")
		else:
			raise errors.SystemNotSet("Please set your system first")
			# return native_gpio.getPinInput(pin.id)

	def output(self, value):
		"""
		Output the desired value to the pin

		value should be (0 or 1).
		native_gpio.outputToPin(pin.id, GPIO._native_high_or_low(value))
		"""
		if (self.is_output):
			raise errors.SystemNotSet("Please set your system first")
		else:
			raise errors.WrongPinType("Pin is set to input")

	def test(self):
		"""
		Returns whether value() is equal to desired_value

		Used for GPIO.watch()
		"""
		return (self.value() == self.desired_value)

	def setup(self):
		"""
		Initialize the pin with the native_gpio
		"""
		raise errors.SystemNotSet("Please set your system first")
		# native_gpio.setup(self.id, native_gpio.OUT if self.is_output else native_gpio.IN)

	def destroy(self):
		"""
		Remove pin configuration through native pin object then drop pin

		Subsequently calls GPIO.drop_pin()
		"""
		raise errors.SystemNotSet("Please set your system first")
		# wrapper.drop_pin(self)


# Generic PWM Pin class
class PWMPin(Pin):
	"""
	Base class for storing GPIO pin configurations and related methods

	Attributes:
		frequency		Array of configured pins
		duty_cycle		Stores Support() instance for system-wide support configurations
		_running		Is pwm running on this pin?
	"""

	frequency = None
	duty_cycle = None
	_running = False

	def setup(self, frequency=self.frequency, duty_cycle=self.duty_cycle):
		"""
		Initialize the PWM pin with the native_gpio
		"""
		# Set attributes to parameters
		self.frequency = frequency
		self.duty_cycle = duty_cycle

		# Raise error since this should be overridden by wrapper derived class
		raise errors.SystemNotSet("Please set your system first")

		# Setup the native pin
		# self.native = native_gpio.PWM(self.id, self.frequency)

	def start(self, duty_cycle=self.duty_cycle):
		"""
		Start PWM at specified duty_cycle
		"""

		# Set attributes to parameters
		self.duty_cycle = duty_cycle

		# Raise error since this should be overridden by wrapper derived class
		raise errors.SystemNotSet("Please set your system first")


		# Start PWM on the native_gpio
		# self.native.start(self.duty_cycle)

		# PWM is running
		self._running = True

	def stop(self):
		"""
		Stop PWM
		"""

		# Raise error since this should be overridden by wrapper derived class
		raise errors.SystemNotSet("Please set your system first")

		# Stop PWM on the native_gpio
		#self.native.stop()

		# PWM is not running
		self._running = False

	def destroy(self):
		"""
		Remove PWM pin configuration through native pin object then drop pin

		Stops PWM on pin, deconfigs, then calls GPIO.drop_pin()
		"""
		raise errors.SystemNotSet("Please set your system first")
		# pwm.stop()
		# wrapper.drop_pin(self)


# Generic module class
class GPIO:
	"""
	Base class for storing GPIO pin configurations and related methods

	Attributes:
		pins			Array of configured pins
		supports		Stores Support() instance for system-wide support configurations
		system			String that identifies the SBC in use
							The name of the wrapper file (no extension)
		native			Native GPIO Library
		_watching		Is the watch() loop running?
							Also used to stop the watch() loop
	"""
	def __init__(self):
		"""
		Sets default values and constructs instance of Pin
		"""
		self.pins = []
		self.supports = Supports()
		self.system = None
		self.native = None
		self._watching = False

	def _native_high_or_low(self, value):
		"""
		Returns LOW or HIGH value from native_gpio

		Value can be (0 or 1) or (True or False)
		"""

		self._require_system_set()
		# return native_gpio.HIGH if value else native_gpio.LOW

	def _require_system_set(self):
		"""
		Raise an exception if the system is not set
		"""
		if not self.system:
			raise errors.SystemNotSet("Please set your system first")

	def setup_pin(self, number, name=None, action=do_nothing, is_output=False):
		"""
		Use this to initialize a pin

		Pins should call their own setup()
		"""
		self._require_system_set()
		pin = Pin(number, name, action, is_output)
		pin.setup()
		self._add_pin(pin)

	def _add_pin(self, pin):
		"""
		Add a pin to the pins array

		Drops the pin if it already exists
		"""
		self.drop_pin(self.pin(id=pin.id))
		self.pins.append(pin)

	def drop_pin(self, pin):
		"""
		Remove a pin configuration

		This should handle pin deconfiguration if required by system
		"""
		self._require_system_set()
		self._remove_pin(pin)

	def _destroy_all_pins(self):
		"""
		Remove all pin configurations

		Calls destroy() on all pins
		"""
		while self.pins:
			self.pins[0].destroy()

	def _remove_pin(self, pin):
		"""
		Removes a pin from the pins array
		"""
		if pin and (pin in self.pins):
			self.pins.remove(pin)

	def PWM(self, number, freqency, duty_cycle=0, name=None):
		"""
		Use this to initialize a PWM pin

		Use explicit argument for name
		PWM pins should call their own setup()
		"""
		self._require_system_set()
		pwm_pin = PWMPin(number, name)
		pwm_pin.setup(frequency, duty_cycle)
		_add_pin(pwm_pin)

	def _find_pin_by_id(self, id):
		"""
		Return pin from pins array by id
		"""
		for pin in self.pins:
			if id == pin.id:
				return pin
		return False

	def _find_pin_by_number(self, number):
		"""
		Return pin from pins array by number
		"""
		for pin in self.pins:
			if number == pin.number:
				return pin
		return False

	def _find_pin_by_name(self, name):
		"""
		Return pin from pins array by name
		"""
		for pin in self.pins:
			if name == pin.name:
				return pin
		return False

	def pin(self, query=None, id=None):
		"""
		Find a pin in the pins array

		query could be pin.name or pin.number
		Explicitly set id if searching by id
		"""

		if id:
			# Searching by id
			return self._find_pin_by_id(id)

		# Check datatype of query
		if isinstance(query, int):
			# If query is pin.number
			return self._find_pin_by_number(query)

		else:
			# If query is pin.name
			return self._find_pin_by_name(query)

	def cleanup(self):
		"""
		Run the native GPIO cleanup() function if available

		Should also _destroy_all_pins()
		"""
		self._require_system_set()
		self._destroy_all_pins()

	def watch(self, interval=0.15):
		"""
		Watch all pins for their desired_value, and execute pin.action()

		Stops only with a KeyboardInterrupt, changing _watching to False,
			or by killing the process!

		Can also call stop_watching() from signal triggered process
			For example, see ExitHandler.exit()
		"""

		# Set self._watch to handle stop_watching() without watch() first
		self._watching = True

		# Loop through each pin checking its value()
		try:
			# Ensure that breaking out is possible using _watching
			while self._watching:
				# Delay pin value checks to reduce CPU load
				time.sleep(interval)

				# Check each pin
				for pin in self.pins:
					if pin.test():
						pin.action()
		except KeyboardInterrupt:
			# This is currently not being used, see signal.signal
			print("Breaking out of watch()")
			self.stop_watching()

		print("Broke out")

		# Reset self._watching just in case stop_watching wasn't run
		self.stop_watching

	def stop_watching(self):
		"""
		Changes the _watching variable to False to stop watch() if it is running
		"""
		self._watching = False
