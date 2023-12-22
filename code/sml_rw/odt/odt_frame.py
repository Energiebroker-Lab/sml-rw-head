"""
Module to handle ODT-Frames
"""

from smllib.crc import get_crc  # type: ignore
from loguru import logger


class OdtFrame:
    """
    Class to process ODT-type frames and transform them to SML-type frames
    """
    byte_array_odt: bytearray
    byte_array_sml: bytearray
    data = {'1.8.0': None, '2.8.0': None, '16.7.0': None}

    def __init__(self, data: bytearray = bytearray()):
        """
        Constructor
        :param data: A bytearray containing the od frame
        """
        self.byte_array_odt = data

    def add(self, new_byte: bytes):
        """
        Adds new Byte to OD_Stream
        """
        self.byte_array_odt += new_byte

    def _parse(self):
        """
        Parses the bytearray and constructs the OdtFrame
        """
        if len(self.byte_array_odt) == 0 or \
                '!' not in self.byte_array_odt.decode(errors='replace'):
            return
        self.byte_array_odt = self.byte_array_odt.replace(b'\r', b'')
        od_strings = self.byte_array_odt.decode(errors='replace').split('\n')
        for od_string in od_strings:
            if '!' in od_string:
                break
            if '*255(' not in od_string:
                continue
            substring = od_string.split('(')
            if len(substring) > 0:
                substring = substring[1]
            else:
                continue
            substring = substring.split('*')[0]
            if substring == '':
                continue
            if '1.8.0' in od_string:
                value = int(
                    float(substring) * 10000
                )  # transform from kWh to Wh (1 dec place)
                self.data['1.8.0'] = value  # type: ignore

            elif '2.8.0' in od_string:
                value = int(
                    float(substring) * 10000
                )  # transform from kWh to Wh (1 dec place)
                self.data['2.8.0'] = value  # type: ignore
            elif '16.7.0' in od_string:
                value = int(float(substring) * 10)
                self.data['16.7.0'] = value  # type: ignore

        self.byte_array_odt.clear()

    def _generate_crc(self) -> int:
        """
        Runs a CRC16/X-25 operation on the prepared sml frame
        :return: The crc code for the sml frame, high and low byte flipped
        """
        return get_crc(self.byte_array_sml)  # type: ignore

    def to_sml(self) -> bytearray:
        """
        Returns the sml representation of the od frame
        https://www.stefan-weigert.de/php_loader/sml.php
        Scaler:
            ...
            52FE = 10^-2 (x0,01)
            52FF = 10^-1 (x0,1)
            5200 = 10^0 (x1)
            5201 = 10^1 (x10)
            ...
        :return: The bytearray containing the sml frame
        """
        self._parse()
        obis_count = 0
        if self.data['1.8.0'] is not None:
            obis_count += 1
        if self.data['2.8.0'] is not None:
            obis_count += 1
        if self.data['16.7.0'] is not None:
            obis_count += 1
        if obis_count == 0:
            return bytearray.fromhex('')
        obis_count |= 0x70
        self.byte_array_sml = bytearray.fromhex(  # header
            '1B1B1B1B'  # escape sequence
            '01010101'  # start sml version 1.0
        )
        self.byte_array_sml += bytearray.fromhex(  # start of main body
            '76'  # list size 6
            '051367FB5A'  # transaction id
            '6200'  # group no
            '6200'  # abort on error
            '72'  # list size 2
            '630701'  # get list response
            '77'  # list size 7
            '01'  # client id
            '0B040105425A0100020304'  # server id
            '070100620AFFFF'  # list name
            '72'  # list size 2
            '6201'  # choice sec index
            '65035F7798' +  # sec index
            hex(obis_count)[2:]  # list size <obis count>
        )
        if self.data['1.8.0'] is not None:
            value = hex(self.data['1.8.0']  # type: ignore
                        )[2:].zfill(16)
            # remove the leading 0x and fill
            # the string up to 16 letters
            self.byte_array_sml += bytearray.fromhex(
                '77'  # list size 7
                '070100010800FF'  # obis code
                '6500010180'  # status
                '01'  # val time
                '621E'  # unit 1E=Wh
                '52FF'  # scaler
                '59' + value +  # start of value
                '01'  # value signature
            )
        if self.data['2.8.0'] is not None:
            value = hex(self.data['2.8.0'])[2:].zfill(16)  # type: ignore
            # remove the leading 0x and fill
            # the string up to 16 letters
            self.byte_array_sml += bytearray.fromhex(
                '77'  # list size 7
                '070100020800FF'  # obis code
                '6500010180'  # status
                '01'  # val time
                '621E'  # unit 1E=Wh
                '52FF'  # scaler
                '59' + value +  # value
                '01'  # value signature
            )
        if self.data['16.7.0'] is not None:
            if self.data['16.7.0'] > 0:  # type: ignore
                value = hex(abs(self.data['16.7.0']))[2:]  # type: ignore
                value = value.zfill(8)
            else:
                value = hex(
                    abs(0xFFFFFFFF - self.data['16.7.0']  # type: ignore
                        + 1) & 0xFFFFFFFF  # prevent overflow
                )[2:]
                value = value.rjust(8, 'F')
            self.byte_array_sml += bytearray.fromhex(
                '77'  # list size 7
                '070100100700FF'  # obis code
                '01'  # status
                '01'  # val time
                '621B'  # unit 1B=W
                '52FF'  # scaler
                '55' + value +  # value
                '01'  # value signature
            )
        self.byte_array_sml += bytearray.fromhex(
            '01'  # list signature
            '01'  # act gateway time
            '63012C'  # mockup crc (not checked by smllib)
            '00'  # end of inner sml message
            '1B1B1B1B'  # escape sequence
            '1A00'  # start of crc
        )
        self.byte_array_sml += bytearray.fromhex(
            hex(self._generate_crc())[2:].zfill(4)
        )  # crc
        return self.byte_array_sml

    def log(self):
        """
        Logs the frame to the debug channel
        """
        logger.debug(
            f'OD Frame:\n'
            f"1.8.0: {self.data['1.8.0']}\n"
            f"2.8.0: {self.data['2.8.0']}\n"
            f"16.7.0: {self.data['16.7.0']}\n"
        )
