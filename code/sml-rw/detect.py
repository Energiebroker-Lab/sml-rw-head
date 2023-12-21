import serial.tools.list_ports  # For listing available serial ports
import serial  # For serial communication


class DetectSerial:
    def __init__(self, ftdiSerial: str):
        self.ftdiSerial = ftdiSerial
        self.portDevice = None
        self._scan()

    def _scan(self):
        ports = serial.tools.list_ports.comports()
        for w in ports:
            if w.serial_number == self.ftdiSerial:  # Match ID with the correct port
                self.portDevice = w.device  # Store the device name to later open port with.

    def getPort(self):
        return self.portDevice
