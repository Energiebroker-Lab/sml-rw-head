from meters.dd3 import DD3
from meters.ehz import EHZ
from meters.mt175 import MT175
from meters.mt681 import MT681
from loguru import logger


def toggleInfo(meterType: str, ftdiSerial: str, pin: [int, int, int, int]):
    meter = None
    if meterType.lower() == 'mt681':
        meter = MT681(ftdiSerial, pin)
    elif meterType.lower() == 'mt175':
        meter = MT175(ftdiSerial, pin)
    elif meterType.lower() == 'ehz':
        meter = EHZ(ftdiSerial, pin)
    elif meterType.lower() == 'dd3':
        meter = DD3(ftdiSerial, pin)

    if meter is None:
        logger.warning(f'Meter {meterType} is not supported')
        return

    meter.toggleInfoMode()
    del meter
