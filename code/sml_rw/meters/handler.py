"""
Handles toggle info for all meters
"""
from loguru import logger
from meters.dd3 import DD3
from meters.ehz import EHZ
from meters.mt175 import MT175
from meters.mt681 import MT681


def toggle_info(meter_type: str, ftdi_serial: str, pin: [int, int, int, int]):
    """
    Selects the correct logic for the supplied meter and toggles info mode
    :param meter_type: mt681, mt175, ehz, dd3
    :param ftdi_serial: serialnumber of the ftdi device
    :param pin: the pin of the meter
    """
    meter = None
    if meter_type.lower() == 'mt681':
        meter = MT681(ftdi_serial, pin)
    elif meter_type.lower() == 'mt175':
        meter = MT175(ftdi_serial, pin)
    elif meter_type.lower() == 'ehz':
        meter = EHZ(ftdi_serial, pin)
    elif meter_type.lower() == 'dd3':
        meter = DD3(ftdi_serial, pin)


    if meter is None:
        logger.warning(f'Meter {meter_type} is not supported')
        return

    meter.toggleInfoMode()
    del meter
