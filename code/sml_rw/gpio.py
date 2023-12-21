"""
ftdi gpio module
"""
from pyftdi.ftdi import Ftdi


class Gpio:
    """
    controls the gpio of the ftdi device
    """
    ftdi = None
    bitmask = 1 << 3
    direction = 1 << 3

    def open(self, ftdi_serial_number: str):
        """
        opens the ftdi device with the given serial number
        :param ftdi_serial_number: ftdi device serial number
        """
        self.ftdi = Ftdi()
        self.ftdi.open_from_url(f"ftdi://::{ftdi_serial_number}/1")
        self.ftdi.set_cbus_direction(self.bitmask, self.direction)
        self.ftdi.set_bitmode(0, Ftdi.BitMode.CBUS)

    def set_gpio(self, value: int):
        """
        sets the gpio to high or low
        :param value: 0 -> low, 1 -> high
        """
        if self.ftdi is None:
            return
        if value > 0:
            self.ftdi.set_cbus_gpio(self.direction)
        else:
            self.ftdi.set_cbus_gpio(0)

    def close(self):
        """
        closes the ftdi device
        """
        self.ftdi.close()
