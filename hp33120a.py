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
Control an HP / Agilent / Keystone 33120A signal generator
"""
import logging
from hp_common import HpCommon
import time

class HP33120A(HpCommon):

    SIGNAL_GENERATOR_ID = b'33120A'

    @classmethod
    def find_ports(cls):
        """
        Return a list of serial ports for all 33120A signal generators.
        """
        return super.find_ports(cls.SIGNAL_GENERATOR_ID)

    @classmethod
    def find_port(cls):
        """
        Return the first available signal generator or None if none are avaiable
        """
        return HpCommon.find_port(cls.SIGNAL_GENERATOR_ID)

    def set_sin_pp(self, hz, vpp):
        cmd = f'APPL:SIN {hz} HZ, {vpp} VPP\n'
        self.send(bytearray(cmd, 'utf-8'))

    def set_sin_rms(self, hz, vrms):
        cmd = f'APPL:SIN {hz} HZ, {vrms} VRMS\n'
        self.send(bytearray(cmd, 'utf-8'))

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    port = HP33120A.find_port()
    logging.info(f'Found {HP33120A.SIGNAL_GENERATOR_ID} on {port}')
    signal_generator = HP33120A(port)
    signal_generator.setup()
    signal_generator.set_sin_pp(60, 1.0)
    time.sleep(5)
    signal_generator.set_sin_rms(50, 1.0)
    time.sleep(5)
