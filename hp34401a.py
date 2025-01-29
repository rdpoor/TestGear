# MIT License
#
# Copyright (c) 2025 R. Dunbar Poor
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Control an HP / Agilent / Keystone 34401A Digital Multimeter (DMM)
"""
import logging
from hp_common import HpCommon

class HP34401A(HpCommon):

    MULTIMETER_ID = b'34401A'

    @classmethod
    def find_ports(cls):
        """
        Return a list of serial ports for all 34401A digital multimeters.
        """
        return HpCommon.find_ports(cls.MULTIMETER_ID)

    @classmethod
    def find_port(cls):
        """
        Return the first available multimeter or None if none are avaiable
        """
        return HpCommon.find_port(cls.MULTIMETER_ID)

    def read_dc_voltage(self):
        resp = self.query(b'MEAS:VOLT:DC?\n')
        return float(resp)

    def read_ac_voltage(self):
        resp = self.query(b'MEAS:VOLT:AC?\n')
        return float(resp)

    def read_dc_current(self):
        resp = self.query(b'MEAS:CURR:DC?\n')
        return float(resp)

    def read_ac_current(self):
        resp = self.query(b'MEAS:CURR:AC?\n')
        return float(resp)

    def read_frequency(self):
        resp = self.query(b'MEAS:FREQ?\n')
        try:
            return float(resp)
        except ValueError:
            return 0.0

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    port = HP34401A.find_port()
    logging.info(f'Found {HP34401A.MULTIMETER_ID} on {port}')
    dmm = HP34401A(port)
    dmm.setup()
    logging.info(f'dc_voltage = {dmm.read_dc_voltage()}')
    logging.info(f'ac_voltage = {dmm.read_ac_voltage()}')
    logging.info(f'dc_current = {dmm.read_dc_current()}')
    logging.info(f'ac_current = {dmm.read_ac_current()}')
    logging.info(f'frequency = {dmm.read_frequency()}')
