from gpio import Gpio


class Meter:
    _gpio = Gpio()
    _pin = [0, 0, 0, 0]
    _debug = False

    def __init__(self, ftdiSerial: str, pin: [int, int, int, int]):
        self._gpio.open(ftdiSerial)
        self._pin = pin

    def __del__(self):
        self._gpio.close()

    def setDebug(self, debug: bool):
        """ un-/set debug mode
            no initial wait etc. in debug mode
        """
        self._debug = debug
