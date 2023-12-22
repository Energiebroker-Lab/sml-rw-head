"""
DD3-ODT meter logic
"""
from typing import Annotated, List

import serial

from meters.dd3 import DD3
from meters.meter import TelegramType


# pylint: disable=too-few-public-methods
class DD3ODT(DD3):
    """
    Class for the DD3-ODT Meter
    """
    def __init__(self, ftdi_serial: str, pin: Annotated[List[int], 4]):
        super().__init__(ftdi_serial, pin)

        # Public Properties
        self.connection_settings = {
            'baudrate': 9600,
            'parity': serial.PARITY_EVEN,
            'stopbits': serial.STOPBITS_ONE,
            'bytesize': serial.SEVENBITS
        }
        self.telegram_type = TelegramType.OD
