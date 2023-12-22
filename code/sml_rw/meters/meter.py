"""
Meter baseclass
"""
from enum import Enum
from typing import Annotated, List, TypedDict

import serial

from gpio import Gpio


class ConnectionSettings(TypedDict):
    """
    Connection settings for the serial device
    """
    baudrate: int
    parity: str
    stopbits: float
    bytesize: int


class TelegramType(Enum):
    """
    Type of the meter telegram
    """
    SML = 'sml'
    OD = 'od'


class Meter:
    """
    Meter baseclass
    """
    _gpio = Gpio()
    _pin = [0, 0, 0, 0]
    _debug = False

    def __init__(self, ftdi_serial: str, pin: Annotated[List[int], 4]):
        self._gpio.open(ftdi_serial)
        self._pin = pin
        self.connection_settings: ConnectionSettings = {
            'baudrate': 9600,
            'parity': serial.PARITY_NONE,
            'stopbits': serial.STOPBITS_ONE,
            'bytesize': serial.EIGHTBITS
        }
        self.telegram_type: TelegramType = TelegramType.SML

    def __del__(self):
        self._gpio.close()

    def set_debug(self, debug: bool):
        """ un-/set debug mode
            no initial wait etc. in debug mode
        """
        self._debug = debug
