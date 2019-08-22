#
#  --------------------------------------------------------------------------
#   Gurux Ltd
#
#
#
#  Filename: $HeadURL$
#
#  Version: $Revision$,
#                $Date$
#                $Author$
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
import abc

ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})
# pylint: disable=too-many-public-methods
class IGXNative(ABC):
    """
    This class is used to communicate with native serial port class. This is
    reserved for inner use. DO NOT USE.
    """

    @abc.abstractmethod
    def getPortNames(self):
        """Returns available serial ports."""

    @abc.abstractmethod
    def open(self, port):
        """
        Open serial port.

        port: Name of serial port.
        """

    @abc.abstractmethod
    def close(self):
        """
        Close serial port.
        """

    @abc.abstractmethod
    def getBaudRate(self):
        """
        Get baud rate.
        """

    @abc.abstractmethod
    def setBaudRate(self, value):
        """
        Set baud rate.
        """

    @abc.abstractmethod
    def getDataBits(self):
        """Get data bits.
        """

    @abc.abstractmethod
    def setDataBits(self, value):
        """Set amount of data bits.
        value : Amount of data bits.
        """

    @abc.abstractmethod
    def getParity(self):
        """Get parity.
        """

    @abc.abstractmethod
    def setParity(self, value):
        """
        Set parity.
        value : parity.
        """

    @abc.abstractmethod
    def getStopBits(self):
        """
        Get stop bits.
        """

    @abc.abstractmethod
    def setStopBits(self, value):
        """
        Set stop bits.
        value: Amount of stop bits.
        """

    @abc.abstractmethod
    def setBreakState(self, value):
        """
        Set break state.
        value : Is serial port in break state.
        """

    @abc.abstractmethod
    def getRtsEnable(self):
        """
        Get Request To Send state.
        """

    @abc.abstractmethod
    def setRtsEnable(self, value):
        """Set Request To Send state.
        value: Is RTS set.
        """

    @abc.abstractmethod
    def getDtrEnable(self):
        """
        Is Data Terminal ready set.
        """

    @abc.abstractmethod
    def setDtrEnable(self, value):
        """Is Data Terminal ready set.
        value : True, if DTR is set.
        """

    @abc.abstractmethod
    def getDsrHolding(self):
        """
        Get Get Data Set Ready holding flag.
        """

    @abc.abstractmethod
    def getBytesToRead(self):
        """
        Returns amount of bytes to read.
        """

    @abc.abstractmethod
    def getBytesToWrite(self):
        """
        Returns amount of bytes to write.
        """

    @abc.abstractmethod
    def read(self):
        """Read data from serial port to the buffer."""

    @abc.abstractmethod
    def write(self, data):
        """Write data to the serial port."""

    @abc.abstractmethod
    def getCtsHolding(self):
        """Returns Clear To Send holding flag."""

    @abc.abstractmethod
    def getCDHolding(self):
        """Gets the state of the Carrier Detect line for the port."""


    @abc.abstractmethod
    def getHandshake(self):
        """Gets the handshaking protocol for serial port transmission of data."""

    @abc.abstractmethod
    def setHandshake(self, value):
        """Sets the handshaking protocol for serial port transmission of data."""

    @abc.abstractmethod
    def isOpen(self):
        """Is connnection open."""
