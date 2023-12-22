"""
MT175 meter logic
"""
from typing import Annotated, List

from loguru import logger

from meters.mt175 import MT175
from reader.reader import SmlReader


class Mt175Cli:
    """
    MT175 meter logic and config
    """
    meter = None

    def get_meter(self, ftdi_serial: str, pin: Annotated[List[int], 4]):
        """
        stores a meter instance in self.meter
        """
        self.meter = MT175(ftdi_serial, pin)

    def log_cli(self, ftdi_serial: str):
        """
        logs sml to the stdout
        :param ftdi_serial: serial number of the ftdi device
        """
        logger.info('logCli mode')
        if self.meter is None:
            logger.error("Meter instance not initialized")
            return
        sml_reader = SmlReader(
            ftdi_serial,
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
        if self.meter is None:
            logger.error("Meter instance not initialized")
            return
        sml_reader = SmlReader(
            ftdi_serial,
            log_sml=True,
            log_file='logSmlMT175.log',
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
        if self.meter is None:
            logger.error("Meter instance not initialized")
            return
        byte_reader = SmlReader(
            ftdi_serial,
            log_bytes=True,
            log_file='logBytesMT175.log',
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
        if self.meter is None:
            logger.error("Meter instance not initialized")
            return
        self.meter.set_debug(True)
        self.meter.enter_pin()
        del self.meter
