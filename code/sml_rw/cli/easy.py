"""
Easy meter cli
"""
from typing import List, Annotated

from loguru import logger

from meters.easy import Easy
from reader.reader import SmlReader


# pylint: disable=protected-access
class EasyCli:
    """
    Easy meter cli arguments
    """
    meter = None

    def get_meter(self, ftdi_serial: str, pin: Annotated[List[int], 4]):
        """
        stores a meter instance in self.meter
        """
        self.meter = Easy(ftdi_serial, pin)

    def log_cli(self, ftdi_serial: str):
        """
        logs sml to the stdout
        :param ftdi_serial: serial number of the ftdi device
        """
        logger.info('logCli mode')
        self.get_meter(ftdi_serial, [0, 0, 0, 0])
        sml_reader = SmlReader(ftdi_serial,
                               connection_settings=self.meter.connection_settings,
                               telegram_type=self.meter.telegram_type
                               )
        sml_reader.run()
        del self.meter

    def log_sml(self, ftdi_serial: str):
        """
        logs sml to logfile
        :param ftdi_serial: serial number of the ftdi device
        """
        logger.info('log_sml mode')
        self.get_meter(ftdi_serial, [0, 0, 0, 0])
        sml_reader = SmlReader(ftdi_serial,
                               log_sml=True,
                               log_file='logSmlEasy.log',
                               connection_settings=self.meter.connection_settings,
                               telegram_type=self.meter.telegram_type
                               )

        sml_reader.run()
        del self.meter

    def log_bytes(self, ftdi_serial: str):
        """
        logs bytes to logfile
        :param ftdi_serial: serial number of the ftdi device
        """
        logger.info('log_bytes mode')
        self.get_meter(ftdi_serial, [0, 0, 0, 0])
        byte_reader = SmlReader(ftdi_serial,
                                log_bytes=True,
                                log_file='logBytesEasy.log',
                                connection_settings=self.meter.connection_settings,
                                telegram_type=self.meter.telegram_type
                                )
        byte_reader.run()
        del self.meter

    def pin(self, ftdi_serial: str, pin: Annotated[List[int], 4]):
        """
        enters pin of the meter
        :param ftdi_serial: serial number of the ftdi device
        :param pin: the pin of the meter
        """
        self.get_meter(ftdi_serial, pin)
        self.meter.set_debug(True)
        self.meter.enter_pin(pin)
        del self.meter

    def clear(self, ftdi_serial: str, pin: Annotated[List[int], 4], topic: str):
        """
        clears the history of the supplied topic
        :param ftdi_serial: serial number of the ftdi device
        :param pin: the pin of the meter
        :param topic: e or his
        """
        self.get_meter(ftdi_serial, pin)
        self.meter.set_debug(True)
        if topic == 'e':
            self.meter.clear(pin, 'e')
        elif topic == 'his':
            self.meter.toggle(pin, 'his')
        del self.meter

    def show(self, ftdi_serial: str, pin: Annotated[List[int], 4], topic: str):
        """
        shows the supplied topic
        :param ftdi_serial: serial number of the ftdi device
        :param pin: the pin of the meter
        :param topic: the topic (menu_item)
        """
        self.get_meter(ftdi_serial, pin)
        self.meter.set_debug(True)
        if topic == 'e':
            self.meter.show(pin, 'e')
        elif topic == '1d':
            self.meter.show(pin, '1d')
        elif topic == '7d':
            self.meter.show(pin, '7d')
        elif topic == '30d':
            self.meter.show(pin, '30d')
        elif topic == '365d':
            self.meter.show(pin, '365d')
        elif topic == 'info':
            self.meter.show(pin, 'info')
        elif topic == 'p':
            self.meter.show(pin, 'p')
        elif topic == 'pin':
            self.meter.show(pin, 'pin')
        del self.meter

    def toggle(self, ftdi_serial: str, pin: Annotated[List[int], 4], topic: str):
        """
        toggles the supplied topic (menu_item)
        :param ftdi_serial: serial number of the ftdi device
        :param pin: the pin of the meter
        :param topic: info, p or pin
        """
        self.get_meter(ftdi_serial, pin)
        self.meter.set_debug(True)
        if topic == 'info':
            self.meter.toggle(pin, 'info')
        elif topic == 'p':
            self.meter.toggle(pin, 'p')
        elif topic == 'pin':
            self.meter.toggle(pin, 'pin')
        del self.meter

    def interactive(self, ftdi_serial: str, pin: Annotated[List[int], 4]):
        """
        interactive control mode
        :param ftdi_serial: serial number of the ftdi device
        :param pin: the pin of the meter
        """
        try:
            self.get_meter(ftdi_serial, pin)
            self.meter.set_debug(True)
            self.meter.enter_pin(pin)
            print("'exit' to quit")
            exit_loop = False
            while not exit_loop:
                pulse = input("'.' = short pulse, '-' = long pulse, ' ' = pause:")
                for c in pulse:
                    if c == ".":
                        print("sending short pulse")
                        self.meter._short_pulse()
                    elif c == "-":
                        print("sending long pulse")
                        self.meter._long_pulse()
                    elif c == " ":
                        print("sending pause")
                        self.meter._pause()
                    elif c == "exit":
                        exit_loop = True
            del self.meter
        except KeyboardInterrupt:
            if self.meter:
                del self.meter
            logger.info("\nProgramm wurde manuell beendet!\n")
