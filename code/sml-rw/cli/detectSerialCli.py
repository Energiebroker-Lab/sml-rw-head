import serial.tools.list_ports  # For listing available serial ports
import serial  # For serial communication
import usb


class DetectSerialCli:
    ftdiserial = None

    def _scan(self, ftdiSerial: str):
        ports = serial.tools.list_ports.comports()
        port = None
        for w in ports:
            if w.serial_number == ftdiSerial:  # Match ID with the correct port
                port = w  # Store the device name to later open port with.
        return port

    def all(self):
        ports = serial.tools.list_ports.comports()
        print('\nDetected the following serial ports:')
        for w in ports:
            print('Port:%s\tID#:=%s' % (w.device, w.serial_number))

    def serial(self, ftdiSerial: str):
        portDevice = self._scan(ftdiSerial)
        if portDevice is not None:
            print('Port:%s\tID#:=%s' % (portDevice.device, portDevice.serial_number))
        else:
            print("Port with ID: %s is not found!" % ftdiSerial)

    '''
    Filter by self.ftdiSerial
    '''
    def _has_serial(self, dev):
        if self.ftdiSerial is None:
            return False
        devSerial = usb.core._try_get_string(dev, dev.iSerialNumber)
        if devSerial == self.ftdiSerial:
            return True

    '''
    returns usb device with given iSerialNumber
    '''
    def _getUsbDeviceBySerial(self, ftdiSerial: str):
        self.ftdiSerial = ftdiSerial
        device = usb.core.find(custom_match=self._has_serial)
        return device

    '''
    reattach usb device to kernel
    TODO: try catch
    '''
    def reattachUsbDevice(self, ftdiSerial: str):
        device = self._getUsbDeviceBySerial(ftdiSerial)
        if device is not None:
            device.attach_kernel_driver(0)
