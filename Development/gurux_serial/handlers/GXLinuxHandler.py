#
#  --------------------------------------------------------------------------
#   Gurux Ltd
#
#
#
#  Filename: $HeadURL$
#
#  Version: $Revision$,
#                   $Date$
#                   $Author$
#
#  Copyright (c) Gurux Ltd
#
# ---------------------------------------------------------------------------
#
#   DESCRIPTION
#
#  This file is a part of Gurux Device Framework.
#
#  Gurux Device Framework is Open Source software; you can redistribute it
#  and/or modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; version 2 of the License.
#  Gurux Device Framework is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#
#  More information of Gurux products: http://www.gurux.org
#
#  This code is licensed under the GNU General Public License v2.
#  Full text may be retrieved at http://www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------
import glob
import os.path
import os
import fcntl
import array
import termios

from .GXSettings import GXSettings
from .IGXNative import IGXNative

_CMSPAR = 0o10000000000
_BAUDRATE_CONSTANTS = {
        50: termios.B50, 75: termios.B75, 110: termios.B110, 134: termios.B134,
        150: termios.B150, 200: termios.B200, 300: termios.B300,
        600: termios.B600, 1200: termios.B1200, 1800: termios.B1800,
        2400: termios.B2400, 4800: termios.B4800, 9600: termios.B9600,
        19200: termios.B19200, 38400: termios.B38400, 57600: termios.B57600,
        115200: termios.B115200, 230400: termios.B230400,
        # Linux baudrates bits missing in termios module included below
        460800: 0x1004, 500000: 0x1005, 576000: 0x1006,
        921600: 0x1007, 1000000: 0x1008, 1152000: 0x1009,
        1500000: 0x100A, 2000000: 0x100B, 2500000: 0x100C,
        3000000: 0x100D, 3500000: 0x100E, 4000000: 0x100F,
    }

_DATABITS_TO_CFLAG = {
        5: termios.CS5, 6: termios.CS6, 7: termios.CS7, 8: termios.CS8
    }
# pylint: disable=too-many-public-methods,too-many-instance-attributes
class GXLinuxHandler(GXSettings, IGXNative):
    def __init__(self):
        """Constructor."""
        GXSettings.__init__(self)
        self.h = None

    def getPortNames(self):
        """Returns available serial ports."""
        tmp = glob.glob('/dev/ttyS*')
        tmp.extend(glob.glob('/dev/ttyUSB*'))
        tmp.extend(glob.glob('/dev/ttyXRUSB*'))
        tmp.extend(glob.glob('/dev/ttyACM*'))
        tmp.extend(glob.glob('/dev/ttyAMA*'))
        tmp.extend(glob.glob('/dev/rfcomm*'))
        tmp.extend(glob.glob('/dev/ttyAP*'))
        # hide non-present internal serial ports
        devices = []
        for device in tmp:
            if os.access(device, os.R_OK) and os.access(device, os.W_OK):
                devices.append(device)
        return devices

    def isOpen(self):
        return self.h

    def open(self, port):
        #pylint: disable=bare-except
        """
        Open serial port.

        port: Name of serial port.
        """
        self.close()
        if not port:
            raise Exception("Invalid serial port name.")
        self.h = os.open(port, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
        (iflag, oflag, cflag, lflag, ispeed, ospeed, cc) = termios.tcgetattr(self.h)
        # set up raw mode / no echo / binary
        cflag |= (termios.CLOCAL | termios.CREAD)
        lflag &= ~(termios.ICANON | termios.ECHO | termios.ECHOE | \
            termios.ECHOK | termios.ECHONL | \
            termios.ISIG | termios.IEXTEN)  # |termios.ECHOPRT
        oflag &= ~(termios.OPOST | termios.ONLCR | termios.OCRNL)
        iflag &= ~(termios.INLCR | termios.IGNCR | termios.ICRNL | termios.IGNBRK)
        #Baud rate
        ispeed = _BAUDRATE_CONSTANTS[int(self._baudrate)]
        ospeed = _BAUDRATE_CONSTANTS[int(self._baudrate)]
        #Databits
        cflag &= ~termios.CSIZE
        if self._dataBits == 8:
            cflag |= termios.CS8
        elif self._dataBits == 7:
            cflag |= termios.CS7
        elif self._dataBits == 6:
            cflag |= termios.CS6
        elif self._dataBits == 5:
            cflag |= termios.CS5
        #Stop bits
        if int(self._stopBits) == 0:
            cflag &= ~(termios.CSTOPB)
        else:
            cflag |= (termios.CSTOPB)
        # setup parity
        iflag &= ~(termios.INPCK | termios.ISTRIP)
        p = int(self._parity)
        if p == 0: #Parity.NONE
            cflag &= ~(termios.PARENB | termios.PARODD | _CMSPAR)
        elif p == 2: #Parity.PARITY_EVEN
            cflag &= ~(termios.PARODD | _CMSPAR)
            cflag |= (termios.PARENB)
        elif p == 1: #Parity.ODD:
            cflag &= ~_CMSPAR
            cflag |= (termios.PARENB | termios.PARODD)
        elif p == 3 and _CMSPAR:#Parity.MARK
            cflag |= (termios.PARENB | _CMSPAR | termios.PARODD)
        elif p == 4 and _CMSPAR:#Parity.SPACE
            cflag |= (termios.PARENB | _CMSPAR)
            cflag &= ~(termios.PARODD)
        termios.tcsetattr(self.h, termios.TCSANOW, [iflag, oflag, cflag, lflag, ispeed, ospeed, cc])

    def close(self):
        """
        Close serial port.
        """
        if self.h:
            os.close(self.h)
            self.h = None

    def getBaudRate(self):
        """
        Get baud rate.
        """
        try:
            (_, _, _, _, _, rate, _) = termios.tcgetattr(self.h)
        except termios.error as e:
            raise Exception("getBaudRate failed. " + e.strerror)
        for k, v in _BAUDRATE_CONSTANTS.items():
            if v == rate:
                return k
        raise Exception("Unknown baud rate: " + str(rate))

    def setBaudRate(self, value):
        """
        Set baud rate.
        """
        try:
            (iflag, oflag, cflag, lflag, ispeed, ospeed, cc) = termios.tcgetattr(self.h)
        except termios.error as e:
            raise Exception("setBaudRate failed. " + e.strerror)
        cflag &= ~(termios.CBAUD | termios.CBAUDEX)
        cflag |= _BAUDRATE_CONSTANTS[value]
        ispeed = _BAUDRATE_CONSTANTS[value]
        ospeed = _BAUDRATE_CONSTANTS[value]
        try:
            termios.tcsetattr(self.h, termios.TCSANOW, [iflag, oflag, cflag, lflag, ispeed, ospeed, cc])
        except termios.error as e:
            raise Exception("setBaudRate failed. " + e.strerror)

    def getDataBits(self):
        """
        Get data bits.
        """
        try:
            (_, _, cflag, _, _, _, _) = termios.tcgetattr(self.h)
        except termios.error as e:
            raise Exception("getDataBits failed. " + e.strerror)

        cs = cflag & termios.CSIZE
        for k, v in _DATABITS_TO_CFLAG.items():
            if v == cs:
                return k
        raise Exception("Unknown data bits: " + str(cs))

    def setDataBits(self, value):
        """
        Set amount of data bits.
        value : Amount of data bits.
        """
        try:
            (iflag, oflag, cflag, lflag, ispeed, ospeed, cc) = termios.tcgetattr(self.h)
        except termios.error as e:
            raise Exception("setDataBits failed. " + e.strerror)
        cflag &= ~termios.CSIZE
        cflag |= _DATABITS_TO_CFLAG[value]
        try:
            termios.tcsetattr(self.h, termios.TCSANOW, [iflag, oflag, cflag, lflag, ispeed, ospeed, cc])
        except termios.error as e:
            raise Exception("setDataBits failed. " + e.strerror)

    def getParity(self):
        """Get parity.
        """
        try:
            (_, _, cflag, _, _, _, _) = termios.tcgetattr(self.h)
        except termios.error as e:
            raise Exception("getParity failed. " + e.strerror)
        #Parity.MARK
        if (cflag & (termios.PARENB | _CMSPAR | termios.PARODD)) == (termios.PARENB | _CMSPAR | termios.PARODD):
            return 3
        #SPACE
        if (cflag & (termios.PARENB | _CMSPAR)) == (termios.PARENB | _CMSPAR):
            return 4
        #ODD
        if (cflag & (termios.PARENB | termios.PARODD)) == (termios.PARENB | termios.PARODD):
            return 1
        #EVEN
        if (cflag & (termios.PARENB)) == (termios.PARENB):
            return 2
        #NONE
        return 0

    def setParity(self, value):
        """
        Set parity.
        value : parity.
        """
        try:
            (iflag, oflag, cflag, lflag, ispeed, ospeed, cc) = termios.tcgetattr(self.h)
        except termios.error as e:
            raise Exception("setParity failed. " + e.strerror)

        iflag &= ~(termios.INPCK | termios.ISTRIP)
        if self._parity == 0: #Parity.NONE:
            cflag &= ~(termios.PARENB | termios.PARODD | _CMSPAR)
        elif self._parity == 2:#Parity.EVEN:
            cflag &= ~(termios.PARODD | _CMSPAR)
            cflag |= (termios.PARENB)
        elif self._parity == 1: #Parity.ODD:
            cflag &= ~_CMSPAR
            cflag |= (termios.PARENB | termios.PARODD)
        elif self._parity == 3 and _CMSPAR: #Parity.MARK
            cflag |= (termios.PARENB | _CMSPAR | termios.PARODD)
        elif self._parity == 4 and _CMSPAR: #Parity.SPACE
            cflag |= (termios.PARENB | _CMSPAR)
            cflag &= ~(termios.PARODD)
        # Set tty attributes
        try:
            termios.tcsetattr(self.h, termios.TCSANOW, [iflag, oflag, cflag, lflag, ispeed, ospeed, cc])
        except termios.error as e:
            raise Exception("setParity failed. " + e.strerror)

    def getStopBits(self):
        """
        Get stop bits.
        """
        try:
            (_, _, cflag, _, _, _, _) = termios.tcgetattr(self.h)
        except termios.error as e:
            raise Exception("getStopBits failed. " + e.strerror)
        if cflag & termios.CSTOPB != 0:
            return 1
        return 0

    def setStopBits(self, value):
        """
        Set stop bits.
        value: Amount of stop bits.
        """
        try:
            (iflag, oflag, cflag, lflag, ispeed, ospeed, cc) = termios.tcgetattr(self.h)
        except termios.error as e:
            raise Exception("setStopBits failed. " + e.strerror)
        cflag &= ~termios.CSTOPB
        if value == 1:
            cflag |= termios.CSTOPB
        try:
            termios.tcsetattr(self.h, termios.TCSANOW, [iflag, oflag, cflag, lflag, ispeed, ospeed, cc])
        except termios.error as e:
            raise Exception("setStopBits failed. " + e.strerror)

    def setBreakState(self, value):
        """
        Set break state.
        value : Is serial port in break state.
        """

    def getRtsEnable(self):
        """
        Get Request To Send state.
        """
        try:
            (_, _, cflag, _, _, _, _) = termios.tcgetattr(self.h)
        except termios.error as e:
            raise Exception("getCtsHolding failed. " + e.strerror)
        return (cflag & termios.CRTSCTS) != 0

    def setRtsEnable(self, value):
        """Set Request To Send state.
        value: Is RTS set.
        """
        try:
            (iflag, oflag, cflag, lflag, ispeed, ospeed, cc) = termios.tcgetattr(self.h)
        except termios.error as e:
            raise Exception("setRtsEnable failed. " + e.strerror)
        cflag = ~termios.CRTSCTS
        if value:
            cflag |= termios.CRTSCTS
        try:
            termios.tcsetattr(self.h, termios.TCSANOW, [iflag, oflag, cflag, lflag, ispeed, ospeed, cc])
        except termios.error as e:
            raise Exception("setRtsEnable failed. " + e.strerror)

    def getDtrEnable(self):
        """
        Is Data Terminal ready set.
        """
        try:
            (_, _, cflag, _, _, _, _) = termios.tcgetattr(self.h)
        except termios.error as e:
            raise Exception("getCtsHolding failed. " + e.strerror)
        return cflag & termios.CRTSCTS != 0

    def setDtrEnable(self, value):
        """Is Data Terminal ready set.
        value : True, if DTR is set.
        """
        try:
            (iflag, oflag, cflag, lflag, ispeed, ospeed, cc) = termios.tcgetattr(self.h)
        except termios.error as e:
            raise Exception("setRtsEnable failed. " + e.strerror)
        cflag = ~termios.CRTSCTS
        if value:
            cflag |= termios.CRTSCTS
        try:
            termios.tcsetattr(self.h, termios.TCSANOW, [iflag, oflag, cflag, lflag, ispeed, ospeed, cc])
        except termios.error as e:
            raise Exception("setRtsEnable failed. " + e.strerror)

    def getDsrHolding(self):
        """
        Get Get Data Set Ready holding flag.
        """

    def getBytesToRead(self):
        """
        Returns amount of bytes to read.
        """
        buffer = array.array('I', [0])
        fcntl.ioctl(self.h, termios.TIOCINQ, buffer, True)
        return buffer[0]

    def getBytesToWrite(self):
        """
        Returns amount of bytes to write.
        """
        buffer = array.array('I', [0])
        fcntl.ioctl(self.h, termios.TIOCOUTQ, buffer, True)
        return buffer[0]

    def read(self):
        """Read data from serial port to the buffer."""
        return os.read(self.h, 100)

    def write(self, data):
        """Write data to the serial port."""
        return os.write(self.h, data)

    def getCtsHolding(self):
        """Returns Clear To Send holding flag."""
        try:
            (_, _, cflag, _, _, _, _) = termios.tcgetattr(self.h)
        except termios.error as e:
            raise Exception("getCtsHolding failed. " + e.strerror)
        return cflag & termios.CRTSCTS != 0

    def getCDHolding(self):
        """Gets the state of the Carrier Detect line for the port."""

    def getHandshake(self):
        """Gets the handshaking protocol for serial port transmission of data."""

    def setHandshake(self, value):
        # pylint: disable=attribute-defined-outside-init
        """Sets the handshaking protocol for serial port transmission of data."""
