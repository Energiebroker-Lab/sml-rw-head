"""
Meter baseclass
"""
from gpio import Gpio


class Meter:
    """
    Meter baseclass
    """
    _gpio = Gpio()
    _pin = [0, 0, 0, 0]
    _debug = False

    def __init__(self, ftdi_serial: str, pin: [int, int, int, int]):
        self._gpio.open(ftdi_serial)
        self._pin = pin

    def __del__(self):
        self._gpio.close()

    def set_debug(self, debug: bool):
        """ un-/set debug mode
            no initial wait etc. in debug mode
        """
        self._debug = debug
