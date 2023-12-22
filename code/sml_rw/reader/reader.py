"""
sml reader
"""
import sys
from threading import Timer
import serial
import smllib
from loguru import logger
from detect import DetectSerial
from meters.meter import ConnectionSettings, TelegramType


class WatchdogTimer:
    """
    used to separate sml streams
    """
    def __init__(self, timeout: float, user_handler=None):
        self.timeout = timeout
        self.handler = user_handler if user_handler is not None else self.default_handler
        self.timer = Timer(self.timeout, self.handler)
        self.timer.start()

    def reset(self):
        """
        resets the timer
        """
        self.timer.cancel()
        self.timer = Timer(self.timeout, self.handler)
        self.timer.start()

    def stop(self):
        """
        stops the timer
        """
        self.timer.cancel()

    def default_handler(self):
        """
        no handler supplied -> raises Exception
        """
        raise AttributeError


# pylint: disable=too-many-arguments
class SmlReader:
    """
    reader class
    """
    bytes_buffer = b''
    crc16_x25_table = [
        0x0000, 0x1189, 0x2312, 0x329B, 0x4624, 0x57AD, 0x6536, 0x74BF,
        0x8C48, 0x9DC1, 0xAF5A, 0xBED3, 0xCA6C, 0xDBE5, 0xE97E, 0xF8F7,
        0x1081, 0x0108, 0x3393, 0x221A, 0x56A5, 0x472C, 0x75B7, 0x643E,
        0x9CC9, 0x8D40, 0xBFDB, 0xAE52, 0xDAED, 0xCB64, 0xF9FF, 0xE876,
        0x2102, 0x308B, 0x0210, 0x1399, 0x6726, 0x76AF, 0x4434, 0x55BD,
        0xAD4A, 0xBCC3, 0x8E58, 0x9FD1, 0xEB6E, 0xFAE7, 0xC87C, 0xD9F5,
        0x3183, 0x200A, 0x1291, 0x0318, 0x77A7, 0x662E, 0x54B5, 0x453C,
        0xBDCB, 0xAC42, 0x9ED9, 0x8F50, 0xFBEF, 0xEA66, 0xD8FD, 0xC974,
        0x4204, 0x538D, 0x6116, 0x709F, 0x0420, 0x15A9, 0x2732, 0x36BB,
        0xCE4C, 0xDFC5, 0xED5E, 0xFCD7, 0x8868, 0x99E1, 0xAB7A, 0xBAF3,
        0x5285, 0x430C, 0x7197, 0x601E, 0x14A1, 0x0528, 0x37B3, 0x263A,
        0xDECD, 0xCF44, 0xFDDF, 0xEC56, 0x98E9, 0x8960, 0xBBFB, 0xAA72,
        0x6306, 0x728F, 0x4014, 0x519D, 0x2522, 0x34AB, 0x0630, 0x17B9,
        0xEF4E, 0xFEC7, 0xCC5C, 0xDDD5, 0xA96A, 0xB8E3, 0x8A78, 0x9BF1,
        0x7387, 0x620E, 0x5095, 0x411C, 0x35A3, 0x242A, 0x16B1, 0x0738,
        0xFFCF, 0xEE46, 0xDCDD, 0xCD54, 0xB9EB, 0xA862, 0x9AF9, 0x8B70,
        0x8408, 0x9581, 0xA71A, 0xB693, 0xC22C, 0xD3A5, 0xE13E, 0xF0B7,
        0x0840, 0x19C9, 0x2B52, 0x3ADB, 0x4E64, 0x5FED, 0x6D76, 0x7CFF,
        0x9489, 0x8500, 0xB79B, 0xA612, 0xD2AD, 0xC324, 0xF1BF, 0xE036,
        0x18C1, 0x0948, 0x3BD3, 0x2A5A, 0x5EE5, 0x4F6C, 0x7DF7, 0x6C7E,
        0xA50A, 0xB483, 0x8618, 0x9791, 0xE32E, 0xF2A7, 0xC03C, 0xD1B5,
        0x2942, 0x38CB, 0x0A50, 0x1BD9, 0x6F66, 0x7EEF, 0x4C74, 0x5DFD,
        0xB58B, 0xA402, 0x9699, 0x8710, 0xF3AF, 0xE226, 0xD0BD, 0xC134,
        0x39C3, 0x284A, 0x1AD1, 0x0B58, 0x7FE7, 0x6E6E, 0x5CF5, 0x4D7C,
        0xC60C, 0xD785, 0xE51E, 0xF497, 0x8028, 0x91A1, 0xA33A, 0xB2B3,
        0x4A44, 0x5BCD, 0x6956, 0x78DF, 0x0C60, 0x1DE9, 0x2F72, 0x3EFB,
        0xD68D, 0xC704, 0xF59F, 0xE416, 0x90A9, 0x8120, 0xB3BB, 0xA232,
        0x5AC5, 0x4B4C, 0x79D7, 0x685E, 0x1CE1, 0x0D68, 0x3FF3, 0x2E7A,
        0xE70E, 0xF687, 0xC41C, 0xD595, 0xA12A, 0xB0A3, 0x8238, 0x93B1,
        0x6B46, 0x7ACF, 0x4854, 0x59DD, 0x2D62, 0x3CEB, 0x0E70, 0x1FF9,
        0xF78F, 0xE606, 0xD49D, 0xC514, 0xB1AB, 0xA022, 0x92B9, 0x8330,
        0x7BC7, 0x6A4E, 0x58D5, 0x495C, 0x3DE3, 0x2C6A, 0x1EF1, 0x0F78
    ]

    def __init__(
            self,
            ftdi_serial,
            log_sml: bool = False,
            log_bytes: bool = False,
            log_file='reader.log',
            connection_settings: ConnectionSettings = None,
            telegram_type: TelegramType = 'sml'
    ):
        self.ftdi_serial = ftdi_serial
        self.log_sml = log_sml
        self.log_bytes = log_bytes
        self.log_file = log_file
        self.connection_settings = connection_settings
        self.telegram_type = telegram_type

    def watchdog_timer_ovf(self, only_obis: bool = False):
        """
        Called when the sml stream ends
        :param only_obis: True -> extrace only the obis values
        """
        if self.log_bytes:
            with open(self.log_file, "ab") as myfile:
                myfile.write(self.bytes_buffer)
        stream = smllib.SmlStreamReader()
        stream.add(self.bytes_buffer)
        sml_frame = stream.get_frame()
        if sml_frame is None:
            logger.info('Bytes missing')
            return

        if only_obis:
            # Shortcut to extract all values without parsing the whole frame
            obis_values = sml_frame.get_obis()
            for msg in obis_values:
                # prints a nice overview over the received values
                logger.info('Obis: {}', msg.get_value())

        else:
            # return all values but slower
            parsed_msgs = sml_frame.parse_frame()
            for msg in parsed_msgs:
                # prints a nice overview over the received values
                logger.info('Frame: {}', msg.format_msg())
                if self.log_sml:
                    with open(self.log_file, "a", encoding="utf-8") as myfile:
                        myfile.write(msg.format_msg())

    def run(self):
        """
        starts listening to the stream
        """
        try:
            detect_serial = DetectSerial(ftdi_serial=self.ftdi_serial)  # Seriennummer der Lesekopfs
            detect_serial.reattach_usb_device(ftdi_serial=self.ftdi_serial)
            my_tty = serial.Serial(
                port=detect_serial.get_port(),
                timeout=0,
                **self.connection_settings
            )
            logger.info(my_tty.portstr + " geöffnet\n\n")
            my_tty.close()
            my_tty.open()
            try:
                my_tty.reset_input_buffer()
                my_tty.reset_output_buffer()
                watchdog = WatchdogTimer(0.1, self.watchdog_timer_ovf)
                watchdog.stop()
                while True:
                    while my_tty.in_waiting > 0:
                        self.bytes_buffer += my_tty.read()
                        watchdog.reset()

            except KeyboardInterrupt:
                my_tty.close()
                logger.info("\nProgramm wurde manuell beendet!\n")

        except (IOError, TypeError) as e:
            logger.info("serieller Port konnte nicht geöffnet werden: ", e.__traceback__)
            sys.exit()
