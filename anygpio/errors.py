# Error definitions
class SystemNotSet(Exception):
    pass

class WrongPinType(Exception):
    pass

class NoNativeGPIO(Exception):
    pass

class WrapperError(Exception):
    pass
