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
Support for controlling HP / Agilent / Keystone test instruments via Serial ports.
"""
import logging
import serial
import serial.tools.list_ports
import time

class HpCommon:

    VID = 0x0403  # FTDI serial to USB adapter
    PID = 0x6015  # FTDI serial to USB adapter
    BAUD = 9600
    SERIAL_TIMEOUT = 2.0
    HOLDOFF_S = 0.2       # time to wait after sending a command

    @classmethod
    def find_ports(cls, test_instrument_id):
        """
        Return a list of serial ports for all test gear with test_instrument_id
        in the *IDN? response, e.g. '33120A' or '34401A'. Probes each FTDI port.
        """
        test_instruments = []
        ports = serial.tools.list_ports.comports()
        ftdi_ports = [port.device for port in ports if port.vid == cls.VID and port.pid == cls.PID]
        for port in ftdi_ports:
            try:
                with serial.Serial(port, cls.BAUD, timeout=cls.SERIAL_TIMEOUT) as ser:
                    ser.write(b'*IDN?\n')
                    resp = ser.readline()
                    logging.debug(f'find_ports() got {resp}')
                    if test_instrument_id in resp:
                        test_instruments.append(port)
            except serial.serialutil.SerialException:
                logging.warn(f'Port {port} is unavailable - skipping')
        return test_instruments

    @classmethod
    def find_port(cls, test_instrument_id):
        """
        Return the first available test instrument or None if none are avaiable.
        """
        try:
            return cls.find_ports(test_instrument_id)[0]
        except IndexError:
            return None

    def __init__(self, port):
        self._port = port
        self._ser = serial.Serial()

    def open(self):
        if not self._ser.is_open:
            self._ser.baudrate = self.BAUD
            self._ser.port = self._port
            self._ser.timeout = self.SERIAL_TIMEOUT
            self._ser.open()
            logging.info(f'Opened test_instrument port: {self._ser}')

    def close(self):
        if self._ser.is_open:
            self._ser.close()
            logging.info(f'Closed test_instrument port: {self._ser}')

    def setup(self):
        self.send(b'*RST\n')        # reset
        self.send(b'SYST:REM\n')    # remote mode
        self.send(b'*CLS\n')        # clear error queue

    def send(self, bytes):
        self._xfer(bytes, False)

    def query(self, bytes):
        return self._xfer(bytes, True)

    def _xfer(self, bytes, expect_response=False):
        self.open()
        logging.debug(f'test_instrument request={bytes}')
        self._ser.write(bytes)
        if expect_response:
            resp = self._ser.readline()
            logging.debug(f'test_instrument response={resp}')
            return resp
        else:
            time.sleep(self.HOLDOFF_S)

