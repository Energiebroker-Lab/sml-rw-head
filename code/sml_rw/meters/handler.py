"""
Handles toggle info for all meters
"""
from typing import Annotated, List

from loguru import logger

from meters.dd3_odt import DD3ODT
from meters.dd3_odt_2way import DD3ODT2Way
from meters.dd3_sml import DD3SML
from meters.dd3_sml_2way import DD3SML2Way
from meters.ehz import EHZ
from meters.mt175 import MT175
from meters.mt681 import MT681


def toggle_info(meter_type: str, ftdi_serial: str, pin: Annotated[List[int], 4]):
    """
    Selects the correct logic for the supplied meter and toggles info mode
    :param meter_type: mt681, mt175, ehz, dd3
    :param ftdi_serial: serialnumber of the ftdi device
    :param pin: the pin of the meter
    """
    meter = None
    match(meter_type.lower()):
        case 'mt681':
            meter = MT681(ftdi_serial, pin)
        case 'mt175':
            meter = MT175(ftdi_serial, pin)
        case 'ehz':
            meter = EHZ(ftdi_serial, pin)
        case 'dd3_sml':
            meter = DD3SML(ftdi_serial, pin)
        case 'dd3_sml_2way':
            meter = DD3SML2Way(ftdi_serial, pin)
        case 'dd3_odt':
            meter = DD3ODT(ftdi_serial, pin)
        case 'dd3_odt_2way':
            meter = DD3ODT2Way(ftdi_serial, pin)

    if meter is None:
        logger.warning(f'Meter {meter_type} is not supported')
        return

    meter.toggle_info_mode()
    del meter
