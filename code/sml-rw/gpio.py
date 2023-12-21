from pyftdi.ftdi import Ftdi


class Gpio:
    ftdi = None
    bitmask = 1 << 3
    direction = 1 << 3

    def open(self, ftdiSerialNumber: str):
        self.ftdi = Ftdi()
        self.ftdi.open_from_url(f"ftdi://::{ftdiSerialNumber}/1")
        self.ftdi.set_cbus_direction(self.bitmask, self.direction)
        self.ftdi.set_bitmode(0, Ftdi.BitMode.CBUS)

    def setGpio(self, value: int):
        if value > 0:
            self.ftdi.set_cbus_gpio(self.direction)
        else:
            self.ftdi.set_cbus_gpio(0)

    def close(self):
        self.ftdi.close()
