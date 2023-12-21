from loguru import logger
from meters.dd3 import DD3
from reader.reader import SmlReader


class Dd3Cli:
    def logCli(self, ftdiSerial: str):
        logger.info('logCli mode')
        smlReader = SmlReader(ftdiSerial)
        smlReader.run()

    def logSml(self, ftdiSerial: str):
        logger.info('logSml mode')
        smlReader = SmlReader(ftdiSerial, logSml=True, logFile='logSmlDd3.log')

        smlReader.run()

    def logBytes(self, ftdiSerial: str):
        logger.info('logBytes mode')
        byteReader = SmlReader(ftdiSerial, logBytes=True, logFile='logBytesDd3.log')
        byteReader.run()

    def pin(self, ftdiSerial: str, pin: [int, int, int, int]):
        meter = DD3(ftdiSerial, pin)
        meter.setDebug(True)
        meter.enterPin()
        del meter

    def clear(self, ftdiSerial: str, pin: [int, int, int, int], topic: str):
        meter = DD3(ftdiSerial, pin)
        meter.setDebug(True)
        if topic == 'e':
            meter.clear('e')
        elif topic == 'his':
            meter.toggle('his')
        del meter

    def show(self, ftdiSerial: str, pin: [int, int, int, int], topic: str):
        meter = DD3(ftdiSerial, pin)
        meter.setDebug(True)
        meter.show(topic)
        del meter

    def toggle(self, ftdiSerial: str, pin: [int, int, int, int], topic: str):
        meter = DD3(ftdiSerial, pin)
        meter.setDebug(True)
        meter.toggle(topic)
        del meter

    def interactive(self, ftdiSerial: str, pin: [int, int, int, int]):
        try:
            meter = DD3(ftdiSerial, pin)
            meter.setDebug(True)
            meter.enterPin()
            print("'exit' to quit")
            exitLoop = False
            while not exitLoop:
                pulse = input("'.' = short pulse, '-' = long pulse, ' ' = pause:")
                for c in pulse:
                    if c == ".":
                        print("sending short pulse")
                        meter._shortPulse()
                    elif c == "-":
                        print("sending long pulse")
                        meter._longPulse()
                    elif c == " ":
                        print("sending pause")
                        meter._pause()
                    elif c == "exit":
                        exitLoop = True
            del meter
        except KeyboardInterrupt:
            del meter
            logger.info("\nProgramm wurde manuell beendet!\n")
