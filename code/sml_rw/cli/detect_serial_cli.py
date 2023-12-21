"""
FTDI cli
"""
import serial  # For serial communication
import serial.tools.list_ports  # For listing available serial ports
import usb
from serial.tools.list_ports_common import ListPortInfo


# pylint: disable=protected-access
class DetectSerialCli:
    """
    Class to detect and reattach ftdi devices
    """
    _ftdi_serial = None

    def _scan(self, ftdi_serial: str) -> ListPortInfo:
        """
        scans for a device with the given serial
        :param ftdi_serial: serialnumber of the ftdi device
        :return: the port or serial device
        """
        ports = serial.tools.list_ports.comports()
        port = None
        for w in ports:
            if w.serial_number == ftdi_serial:  # Match ID with the correct port
                port = w  # Store the device name to later open port with.
        return port

    def all(self):
        """
        scans for all serial devices and prints the device and serial
        """
        ports = serial.tools.list_ports.comports()
        print('\nDetected the following serial ports:')
        for w in ports:
            print(f"Port:{w.device}\tID#:={w.serial_number}")

    def serial(self, ftdi_serial: str):
        """
        scans for a device with the given serial
        :param ftdi_serial:
        :return:
        """
        port_device = self._scan(ftdi_serial)
        if port_device is not None:
            print(f"Port:{port_device.device}\tID#:={port_device.serial_number}")
        else:
            print(f"Port with ID: {ftdi_serial} is not found!")

    def _has_serial(self, dev) -> bool:
        """
        Filter by self._ftdi_serial
        :param dev: device
        :return: True if the device has the serial number self._ftdi_serial
        """
        if self._ftdi_serial is None:
            return False
        dev_serial = usb.core._try_get_string(dev, dev.iSerialNumber)
        if dev_serial == self._ftdi_serial:
            return True
        return False

    def _get_usb_device_by_serial(self, ftdi_serial: str):
        """
        returns usb device with given serial number
        :param ftdi_serial: serial number of the ftdi device
        """
        self._ftdi_serial = ftdi_serial
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
