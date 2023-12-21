"""
ftdi detection module
"""
import serial  # For serial communication
import serial.tools.list_ports  # For listing available serial ports


# pylint: disable=too-few-public-methods
class DetectSerial:
    """
    Scans for the ftdi device with the supplied serial number
    """
    def __init__(self, ftdi_serial: str):
        self.ftdi_serial = ftdi_serial
        self.port_device = None
        self._scan()

    def _scan(self):
        """
        scans for all ftdi devices and stores the device with the correct serial number
        """
        ports = serial.tools.list_ports.comports()
        for w in ports:
            if w.serial_number == self.ftdi_serial:  # Match ID with the correct port
                self.port_device = w.device  # Store the device name to later open port with.

    def get_port(self) -> str:
        """
        returns the device with the correct serial number
        :return: Serial port
        """
        return self.port_device
