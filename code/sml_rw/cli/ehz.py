"""
EHZ meter cli
"""
from typing import List, Annotated

from loguru import logger

from meters.ehz import EHZ
from reader.reader import SmlReader


class EhzCli:
    """
    EHZ meter cli arguments
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
        sml_reader = SmlReader(ftdi_serial, log_sml=True, log_file='logSmlEhz.log')
        sml_reader.run()

    def log_bytes(self, ftdi_serial: str):
        """
        logs bytes to logfile
        :param ftdi_serial: serial number of the ftdi device
        """
        logger.info('log_bytes mode')
        byte_reader = SmlReader(ftdi_serial, log_bytes=True, log_file='logBytesEhz.log')
        byte_reader.run()

    def pin(self, ftdi_serial: str, pin: Annotated[List[int], 4]):
        """
        enters pin of the meter
        :param ftdi_serial: serial number of the ftdi device
        :param pin: the pin of the meter
        """
        meter = EHZ(ftdi_serial, pin)
        meter.set_debug(True)
        meter.enter_pin()
        del meter
