from loguru import logger
from gpio import Gpio
from meters.ehz import EHZ
from reader.reader import SmlReader


class EhzCli:
    def logCli(self, ftdiSerial: str):
        logger.info('logCli mode')
        smlReader = SmlReader(ftdiSerial)
        smlReader.run()

    def logSml(self, ftdiSerial: str):
        logger.info('logSml mode')
        smlReader = SmlReader(ftdiSerial, logSml=True, logFile='logSmlEhz.log')

        smlReader.run()

    def logBytes(self, ftdiSerial: str):
        logger.info('logBytes mode')
        byteReader = SmlReader(ftdiSerial, logBytes=True, logFile='logBytesEhz.log')
        byteReader.run()

    def pin(self, ftdiSerial: str, pin: [int, int, int, int]):
        meter = EHZ(ftdiSerial, pin)
        meter.setDebug(True)
        meter.enterPin()
        del meter
