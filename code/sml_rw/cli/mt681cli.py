"""
MT681 meter cli
"""
from loguru import logger

from meters.mt681 import MT681
from reader.reader import SmlReader


class Mt681Cli:
    """
    MT681 meter cli arguments
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
        sml_reader = SmlReader(ftdi_serial, log_sml=True, log_file='logSmlMT681.log')
        sml_reader.run()

    def log_bytes(self, ftdi_serial: str):
        """
        logs bytes to logfile
        :param ftdi_serial: serial number of the ftdi device
        """
        logger.info('log_bytes mode')
        byte_reader = SmlReader(ftdi_serial, log_bytes=True, log_file='logBytesMT681.log')
        byte_reader.run()

    def pin(self, ftdi_serial: str, pin: [int, int, int, int]):
        """
        enters pin of the meter
        :param ftdi_serial: serial number of the ftdi device
        :param pin: the pin of the meter
        """
        meter = MT681(ftdi_serial, pin)
        meter.set_debug(True)
        meter.enter_pin()
        del meter