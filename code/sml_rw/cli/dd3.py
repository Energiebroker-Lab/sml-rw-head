"""
DD3 meter cli
"""
from typing import List, Annotated

from loguru import logger

from meters.dd3_odt import DD3ODT
from meters.dd3_odt_2way import DD3ODT2Way
from meters.dd3_sml import DD3SML
from meters.dd3_sml_2way import DD3SML2Way
from reader.reader import SmlReader


# pylint: disable=protected-access
class Dd3Cli:
    """
    DD3 meter cli arguments
    """
    meter = None

    def get_meter(self, ftdi_serial: str, pin: Annotated[List[int], 4]):
        """
        stores a meter instance in self.meter
        """
        raise NotImplementedError

    def log_cli(self, ftdi_serial: str):
        """
        logs sml to the stdout
        :param ftdi_serial: serial number of the ftdi device
        """
        logger.info('logCli mode')
        self.get_meter(ftdi_serial, [0, 0, 0, 0])
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
        self.get_meter(ftdi_serial, [0, 0, 0, 0])
        if self.meter is None:
            logger.error("Meter instance not initialized")
            return
        sml_reader = SmlReader(
            ftdi_serial,
            log_sml=True,
            log_file='logSmlDd3.log',
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
        if self.meter is None:
            logger.error("Meter instance not initialized")
            return
        byte_reader = SmlReader(
            ftdi_serial,
            log_bytes=True,
            log_file='logBytesDd3.log',
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

    def clear(self, ftdi_serial: str, pin: Annotated[List[int], 4], topic: str):
        """
        clears the history of the supplied topic
        :param ftdi_serial: serial number of the ftdi device
        :param pin: the pin of the meter
        :param topic: e or his
        """
        self.get_meter(ftdi_serial, pin)
        if self.meter is None:
            logger.error("Meter instance not initialized")
            return
        self.meter.set_debug(True)
        if topic == 'e':
            self.meter.clear('e')
        elif topic == 'his':
            self.meter.toggle('his')
        del self.meter

    def show(self, ftdi_serial: str, pin: Annotated[List[int], 4], topic: str):
        """
        shows the supplied topic
        :param ftdi_serial: serial number of the ftdi device
        :param pin: the pin of the meter
        :param topic: the topic (menu_item)
        """
        self.get_meter(ftdi_serial, pin)
        if self.meter is None:
            logger.error("Meter instance not initialized")
            return
        self.meter.set_debug(True)
        self.meter.show(topic)
        del self.meter

    def toggle(self, ftdi_serial: str, pin: Annotated[List[int], 4], topic: str):
        """
        toggles the supplied topic (menu_item)
        :param ftdi_serial: serial number of the ftdi device
        :param pin: the pin of the meter
        :param topic: info, p or pin
        """
        self.get_meter(ftdi_serial, pin)
        if self.meter is None:
            logger.error("Meter instance not initialized")
            return
        self.meter.set_debug(True)
        self.meter.toggle(topic)
        del self.meter

    def interactive(self, ftdi_serial: str, pin: Annotated[List[int], 4]):
        """
        interactive control mode
        :param ftdi_serial: serial number of the ftdi device
        :param pin: the pin of the meter
        """
        try:
            self.get_meter(ftdi_serial, pin)
            if self.meter is None:
                logger.error("Meter instance not initialized")
                return
            self.meter.set_debug(True)
            self.meter.enter_pin()
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


class Dd3CliSML(Dd3Cli):
    """
    DD3 meter SML
    """
    meter = None

    def get_meter(self, ftdi_serial: str, pin: Annotated[List[int], 4]):
        """
        stores a meter instance in self.meter
        """
        self.meter = DD3SML(ftdi_serial, pin)


class Dd3CliSML2Way(Dd3Cli):
    """
    DD3 meter SML two-way
    """
    meter = None

    def get_meter(self, ftdi_serial: str, pin: Annotated[List[int], 4]):
        """
        stores a meter instance in self.meter
        """
        self.meter = DD3SML2Way(ftdi_serial, pin)


class Dd3CliODT(Dd3Cli):
    """
    DD3 meter ODT
    """
    meter = None

    def get_meter(self, ftdi_serial: str, pin: Annotated[List[int], 4]):
        """
        stores a meter instance in self.meter
        """
        self.meter = DD3ODT(ftdi_serial, pin)


class Dd3CliODT2Way(Dd3Cli):
    """
    DD3 meter ODT two-way
    """
    meter = None

    def get_meter(self, ftdi_serial: str, pin: Annotated[List[int], 4]):
        """
        stores a meter instance in self.meter
        """
        self.meter = DD3ODT2Way(ftdi_serial, pin)
