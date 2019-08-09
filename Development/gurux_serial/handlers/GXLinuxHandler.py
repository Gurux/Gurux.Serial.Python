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
from .GXSettings import GXSettings
from .IGXNative import IGXNative

#Constant values.
INVALID_HANDLE_VALUE = -1

# pylint: disable=too-many-public-methods,too-many-instance-attributes
class GXLinuxHandler(GXSettings, IGXNative):
    def __init__(self):
        """Constructor."""
        GXSettings.__init__(self)
        self.h = INVALID_HANDLE_VALUE

    def getPortNames(self):
        """Returns available serial ports."""

    def open(self, port):
        #pylint: disable=bare-except
        """
        Open serial port.

        port: Name of serial port.
        """
        self.close()
        if not port:
            raise Exception("Invalid serial port name.")

    def close(self):
        """
        Close serial port.
        """
        if self.h != INVALID_HANDLE_VALUE:
            self.h = INVALID_HANDLE_VALUE

    def getBaudRate(self):
        """
        Get baud rate.
        """


    def setBaudRate(self, value):
        """
        Set baud rate.
        """


    def getDataBits(self):
        """Get data bits.
        """

    def setDataBits(self, value):
        """Set amount of data bits.
        value : Amount of data bits.
        """

    def getParity(self):
        """Get parity.
        """

    def setParity(self, value):
        """
        Set parity.
        value : parity.
        """

    def getStopBits(self):
        """
        Get stop bits.
        """

    def setStopBits(self, value):
        """
        Set stop bits.
        value: Amount of stop bits.
        """

    def setBreakState(self, value):
        """
        Set break state.
        value : Is serial port in break state.
        """

    def getRtsEnable(self):
        """
        Get Request To Send state.
        """

    def setRtsEnable(self, value):
        """Set Request To Send state.
        value: Is RTS set.
        """

    def getDtrEnable(self):
        """
        Is Data Terminal ready set.
        """

    def setDtrEnable(self, value):
        """Is Data Terminal ready set.
        value : True, if DTR is set.
        """

    def getDsrHolding(self):
        """
        Get Get Data Set Ready holding flag.
        """

    def getBytesToRead(self):
        """
        Returns amount of bytes to read.
        """

    def getBytesToWrite(self):
        """
        Returns amount of bytes to write.
        """

    def read(self):
        """Read data from serial port to the buffer."""
        if self.h == INVALID_HANDLE_VALUE:
            raise Exception("Serial port is not open")

    def write(self, data):
        """Write data to the serial port."""
        if self.h == INVALID_HANDLE_VALUE:
            raise Exception("Serial port is not open")

    def getCtsHolding(self):
        """Returns Clear To Send holding flag."""

    def getCDHolding(self):
        """Gets the state of the Carrier Detect line for the port."""

    def getHandshake(self):
        """Gets the handshaking protocol for serial port transmission of data."""

    def setHandshake(self, value):
        # pylint: disable=attribute-defined-outside-init
        """Sets the handshaking protocol for serial port transmission of data."""
