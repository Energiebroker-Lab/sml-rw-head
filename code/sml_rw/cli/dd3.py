"""
DD3 meter cli
"""
from typing import List, Annotated

from loguru import logger

from meters.dd3 import DD3
from reader.reader import SmlReader


# pylint: disable=protected-access
class Dd3Cli:
    """
    DD3 meter cli arguments
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
        sml_reader = SmlReader(ftdi_serial, log_sml=True, log_file='logSmlDd3.log')

        sml_reader.run()

    def log_bytes(self, ftdi_serial: str):
        """
        logs bytes to logfile
        :param ftdi_serial: serial number of the ftdi device
        """
        logger.info('log_bytes mode')
        byte_reader = SmlReader(ftdi_serial, log_bytes=True, log_file='logBytesDd3.log')
        byte_reader.run()

    def pin(self, ftdi_serial: str, pin: Annotated[List[int], 4]):
        """
        enters pin of the meter
        :param ftdi_serial: serial number of the ftdi device
        :param pin: the pin of the meter
        """
        meter = DD3(ftdi_serial, pin)
        meter.set_debug(True)
        meter.enter_pin()
        del meter

    def clear(self, ftdi_serial: str, pin: Annotated[List[int], 4], topic: str):
        """
        clears the history of the supplied topic
        :param ftdi_serial: serial number of the ftdi device
        :param pin: the pin of the meter
        :param topic: e or his
        """
        meter = DD3(ftdi_serial, pin)
        meter.set_debug(True)
        if topic == 'e':
            meter.clear('e')
        elif topic == 'his':
            meter.toggle('his')
        del meter

    def show(self, ftdi_serial: str, pin: Annotated[List[int], 4], topic: str):
        """
        shows the supplied topic
        :param ftdi_serial: serial number of the ftdi device
        :param pin: the pin of the meter
        :param topic: the topic (menu_item)
        """
        meter = DD3(ftdi_serial, pin)
        meter.set_debug(True)
        meter.show(topic)
        del meter

    def toggle(self, ftdi_serial: str, pin: Annotated[List[int], 4], topic: str):
        """
        toggles the supplied topic (menu_item)
        :param ftdi_serial: serial number of the ftdi device
        :param pin: the pin of the meter
        :param topic: info, p or pin
        """
        meter = DD3(ftdi_serial, pin)
        meter.set_debug(True)
        meter.toggle(topic)
        del meter

    def interactive(self, ftdi_serial: str, pin: Annotated[List[int], 4]):
        """
        interactive control mode
        :param ftdi_serial: serial number of the ftdi device
        :param pin: the pin of the meter
        """
        try:
            meter = DD3(ftdi_serial, pin)
            meter.set_debug(True)
            meter.enter_pin()
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
            del meter
        except KeyboardInterrupt:
            del meter
            logger.info("\nProgramm wurde manuell beendet!\n")
