from loguru import logger
from gpio import Gpio
from meters.mt681 import MT681
from reader.reader import SmlReader


class Mt681Cli:
    def logCli(self, ftdiSerial: str):
        logger.info('logCli mode')
        smlReader = SmlReader(ftdiSerial)
        smlReader.run()

    def logSml(self, ftdiSerial: str):
        logger.info('logSml mode')
        smlReader = SmlReader(ftdiSerial, logSml=True, logFile='logSmlMT681.log')

        smlReader.run()

    def logBytes(self, ftdiSerial: str):
        logger.info('logBytes mode')
        byteReader = SmlReader(ftdiSerial, logBytes=True, logFile='logBytesMT681.log')
        byteReader.run()

    def pin(self, ftdiSerial: str, pin: [int, int, int, int]):
        meter = MT681(ftdiSerial, pin)
        meter.setDebug(True)
        meter.enterPin()
        del meter
