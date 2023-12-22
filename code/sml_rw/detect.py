"""
ftdi detection module
"""
import serial  # For serial communication
import serial.tools.list_ports  # For listing available serial ports
import usb


# pylint: disable=too-few-public-methods, protected-access
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

    def get_port(self) -> str | None:
        """
        returns the device with the correct serial number
        :return: Serial port
        """
        return self.port_device

    def _has_serial(self, dev) -> bool:
        """
        Filter by self._ftdi_serial
        :param dev: device
        :return: True if the device has the serial number self._ftdi_serial
        """
        if self.ftdi_serial is None:
            return False
        dev_serial = usb.core._try_get_string(dev, dev.iSerialNumber)
        if dev_serial == self.ftdi_serial:
            return True
        return False

    def _get_usb_device_by_serial(self, ftdi_serial: str):
        """
        returns usb device with given serial number
        :param ftdi_serial: serial number of the ftdi device
        """
        self.ftdi_serial = ftdi_serial
        device = usb.core.find(custom_match=self._has_serial)
        return device

    def reattach_usb_device(self, ftdi_serial: str):
        """
        reattach usb device to kernel
        :param ftdi_serial: serialnumber of the ftdi device
        """
        device = self._get_usb_device_by_serial(ftdi_serial)
        if device is not None:
            device.attach_kernel_driver(0)
