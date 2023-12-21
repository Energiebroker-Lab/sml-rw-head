"""
Easy meter cli
"""
from typing import List, Annotated

from loguru import logger

from gpio import Gpio
from meters.easy import Easy
from reader.reader import SmlReader


# pylint: disable=protected-access
class EasyCli:
    """
    Easy meter cli arguments
    """
    def log_cli(self, ftdi_serial: str):
        """
        logs sml to the stdout
        :param ftdi_serial: serial number of the ftdi device
        """
        logger.info('logCli mode')
        sml_reader = SmlReader(ftdi_serial)
        sml_reader.run()

    def log_sml(self, ftdi_serial: str):
        """
        logs sml to logfile
        :param ftdi_serial: serial number of the ftdi device
        """
        logger.info('log_sml mode')
        sml_reader = SmlReader(ftdi_serial, log_sml=True, log_file='logSmlEasy.log')

        sml_reader.run()

    def log_bytes(self, ftdi_serial: str):
        """
        logs bytes to logfile
        :param ftdi_serial: serial number of the ftdi device
        """
        logger.info('log_bytes mode')
        byte_reader = SmlReader(ftdi_serial, log_bytes=True, log_file='logBytesEasy.log')
        byte_reader.run()

    def pin(self, ftdi_serial: str, pin: Annotated[List[int], 4]):
        """
        enters pin of the meter
        :param ftdi_serial: serial number of the ftdi device
        :param pin: the pin of the meter
        """
        g = Gpio()
        g.open(ftdi_serial)
        meter = Easy(g)
        meter.set_debug(True)
        meter.enter_pin(pin)

    def clear(self, ftdi_serial: str, pin: Annotated[List[int], 4], topic: str):
        """
        clears the history of the supplied topic
        :param ftdi_serial: serial number of the ftdi device
        :param pin: the pin of the meter
        :param topic: e or his
        """
        g = Gpio()
        g.open(ftdi_serial)
        meter = Easy(g)
        meter.set_debug(True)
        if topic == 'e':
            meter.clear(pin, 'e')
        elif topic == 'his':
            meter.toggle(pin, 'his')

    def show(self, ftdi_serial: str, pin: Annotated[List[int], 4], topic: str):
        """
        shows the supplied topic
        :param ftdi_serial: serial number of the ftdi device
        :param pin: the pin of the meter
        :param topic: the topic (menu_item)
        """
        g = Gpio()
        g.open(ftdi_serial)
        meter = Easy(g)
        meter.set_debug(True)
        if topic == 'e':
            meter.show(pin, 'e')
        elif topic == '1d':
            meter.show(pin, '1d')
        elif topic == '7d':
            meter.show(pin, '7d')
        elif topic == '30d':
            meter.show(pin, '30d')
        elif topic == '365d':
            meter.show(pin, '365d')
        elif topic == 'info':
            meter.show(pin, 'info')
        elif topic == 'p':
            meter.show(pin, 'p')
        elif topic == 'pin':
            meter.show(pin, 'pin')

    def toggle(self, ftdi_serial: str, pin: Annotated[List[int], 4], topic: str):
        """
        toggles the supplied topic (menu_item)
        :param ftdi_serial: serial number of the ftdi device
        :param pin: the pin of the meter
        :param topic: info, p or pin
        """
        g = Gpio()
        g.open(ftdi_serial)
        meter = Easy(g)
        meter.set_debug(True)
        if topic == 'info':
            meter.toggle(pin, 'info')
        elif topic == 'p':
            meter.toggle(pin, 'p')
        elif topic == 'pin':
            meter.toggle(pin, 'pin')

    def interactive(self, ftdi_serial: str, pin: Annotated[List[int], 4]):
        """
        interactive control mode
        :param ftdi_serial: serial number of the ftdi device
        :param pin: the pin of the meter
        """
        try:
            g = Gpio()
            g.open(ftdi_serial)
            meter = Easy(g)
            meter.set_debug(True)
            meter.enter_pin(pin)
            print("'exit' to quit")
            exit_loop = False
            while not exit_loop:
                pulse = input("'.' = short pulse, '-' = long pulse, ' ' = pause:")
                for c in pulse:
                    if c == ".":
                        print("sending short pulse")
                        meter._short_pulse()
                    elif c == "-":
                        print("sending long pulse")
                        meter._long_pulse()
                    elif c == " ":
                        print("sending pause")
                        meter._pause()
                    elif c == "exit":
                        exit_loop = True
            if g:
                g.close()
        except KeyboardInterrupt:
            if g:
                g.close()
            logger.info("\nProgramm wurde manuell beendet!\n")
