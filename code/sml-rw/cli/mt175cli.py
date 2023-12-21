from loguru import logger
from gpio import Gpio
from meters.mt175 import MT175
from reader.reader import SmlReader


class Mt175Cli:
    def logCli(self, ftdiSerial: str):
        logger.info('logCli mode')
        smlReader = SmlReader(ftdiSerial)
        smlReader.run()

    def logSml(self, ftdiSerial: str):
        logger.info('logSml mode')
        smlReader = SmlReader(ftdiSerial, logSml=True, logFile='logSmlMT175.log')

        smlReader.run()

    def logBytes(self, ftdiSerial: str):
        logger.info('logBytes mode')
        byteReader = SmlReader(ftdiSerial, logBytes=True, logFile='logBytesMT175.log')
        byteReader.run()

    def pin(self, ftdiSerial: str, pin: [int, int, int, int]):
        meter = MT175(ftdiSerial, pin)
        meter.setDebug(True)
        meter.enterPin()
        del meter
