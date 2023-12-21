from loguru import logger
from gpio import Gpio
from meters.easy import Easy
from reader.reader import SmlReader


class EasyCli:
    def logCli(self, ftdiSerial: str):
        logger.info('logCli mode')
        smlReader = SmlReader(ftdiSerial)
        smlReader.run()

    def logSml(self, ftdiSerial: str):
        logger.info('logSml mode')
        smlReader = SmlReader(ftdiSerial, logSml=True, logFile='logSmlEasy.log')

        smlReader.run()

    def logBytes(self, ftdiSerial: str):
        logger.info('logBytes mode')
        byteReader = SmlReader(ftdiSerial, logBytes=True, logFile='logBytesEasy.log')
        byteReader.run()

    def pin(self, ftdiSerial: str, pin: [int, int, int, int]):
        g = Gpio()
        g.open(ftdiSerial)
        meter = Easy(g)
        meter.setDebug(True)
        meter.enterPin(pin)

    def clear(self, ftdiSerial: str, pin: [int, int, int, int], topic: str):
        g = Gpio()
        g.open(ftdiSerial)
        meter = Easy(g)
        meter.setDebug(True)
        if topic == 'e':
            meter.clear(pin, 'e')
        elif topic == 'his':
            meter.toggle(pin, 'his')

    def show(self, ftdiSerial: str, pin: [int, int, int, int], topic: str):
        g = Gpio()
        g.open(ftdiSerial)
        meter = Easy(g)
        meter.setDebug(True)
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

    def toggle(self, ftdiSerial: str, pin: [int, int, int, int], topic: str):
        g = Gpio()
        g.open(ftdiSerial)
        meter = Easy(g)
        meter.setDebug(True)
        if topic == 'info':
            meter.toggle(pin, 'info')
        elif topic == 'p':
            meter.toggle(pin, 'p')
        elif topic == 'pin':
            meter.toggle(pin, 'pin')

    def interactive(self, ftdiSerial: str, pin: [int, int, int, int]):
        try:
            g = Gpio()
            g.open(ftdiSerial)
            meter = Easy(g)
            meter.setDebug(True)
            meter.enterPin(pin)
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
            if g:
                g.close()
        except KeyboardInterrupt:
            if g:
                g.close()
            logger.info("\nProgramm wurde manuell beendet!\n")
