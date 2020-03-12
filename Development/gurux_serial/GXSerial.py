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
import os
import time
import threading
import traceback
import gurux_common.io.BaudRate
import gurux_common.io.Parity
import gurux_common.io.StopBits
from gurux_common.enums import TraceLevel, MediaState, TraceTypes
from gurux_common.IGXMedia import IGXMedia
from gurux_common.MediaStateEventArgs import MediaStateEventArgs
from gurux_common.TraceEventArgs import TraceEventArgs
from gurux_common.PropertyChangedEventArgs import PropertyChangedEventArgs
from gurux_common.ReceiveEventArgs import ReceiveEventArgs
from ._GXSynchronousMediaBase import _GXSynchronousMediaBase
if os.name == 'nt':  # sys.platform == 'win32':
    from ._handlers.GXWindowsHandler import GXWindowsHandler
elif os.name == 'posix':
    from ._handlers.GXLinuxHandler import GXLinuxHandler

# pylint: disable=too-many-public-methods, too-many-instance-attributes,
# too-many-arguments
class GXSerial(IGXMedia):
    def __init__(self,
                 port,
                 baudRate=gurux_common.io.BaudRate.BAUD_RATE_9600,
                 dataBits=8,
                 parity=gurux_common.io.Parity.NONE,
                 stopBits=gurux_common.io.StopBits.ONE):
        """Constructor.
        port : Serial port.
        baudRate : Baud rate.
        dataBits : Data bits.
        parity : Parity.
        stopBits : Stop bits.
        """
        self.__receiveDelay = 0
        self.__asyncWaitTime = 0
        ###Handle to serial port handler.
        self.__h = self.__initialize()
        #Values are saved if port is not open and user try to set them.
        #Serial port baud rate.
        self.__h.baudRate = baudRate
        ###Used data bits.
        self.__h.dataBits = dataBits
        ###Stop bits.
        self.__h.stopBits = stopBits
        ###Used parity.
        self.__h.parity = parity
        self.__portName = port
        self.__syncBase = _GXSynchronousMediaBase(100)
        ###Amount of bytes sent.
        self.__bytesSent = 0
        self.__bytesReceived = 0
        ###Trace level.
        self.__trace = TraceLevel.OFF
        ###End of packet.
        self.__eop = None
        self.__listeners = []
        self.__rtsEnable = False
        self.__handshake = None
        self.__receiver = None
        self.__closing = threading.Event()
        self.__lock = threading.Lock()

    def __getTrace(self):
        return self.__trace

    def __setTrace(self, value):
        self.__trace = value
        self.__syncBase.trace = value

    trace = property(__getTrace, __setTrace)
    """Trace level."""

    def addListener(self, listener):
        self.__listeners.append(listener)

    def removeListener(self, listener):
        self.__listeners.remove(listener)

    def __notifyPropertyChanged(self, info):
        """Notify that property has changed."""
        for it in self.__listeners:
            it.onPropertyChanged(self, PropertyChangedEventArgs(info))

    def __notifyError(self, ex):
        """Notify clients from error occurred."""
        for it in self.__listeners:
            it.onError(self, ex)
            if self.__trace & TraceLevel.ERROR != 0:
                it.onTrace(self, TraceEventArgs(TraceTypes.ERROR, ex))

    def __notifyReceived(self, e):
        """Notify clients from new data received."""
        for it in self.__listeners:
            it.onReceived(self, e)

    def __notifyTrace(self, e):
        """Notify clients from trace events."""
        for it in self.__listeners:
            it.onTrace(self, e)

    @classmethod
    def __initialize(cls):
        ###Initialize Gurux serial port library.
        if os.name == 'nt':
            return GXWindowsHandler()
        if os.name == 'posix':
            return GXLinuxHandler()
        raise ImportError("Sorry: no implementation for your platform ('{}') available".format(os.name))

    @classmethod
    def getPortNames(cls):
        """Gets an array of serial port names for the current computer."""
        return cls.__initialize().getPortNames()

    def getAvailableBaudRates(self):
        # pylint: disable=no-self-use
        """Get baud rates supported by given serial port."""
        return (gurux_common.io.BaudRate.BAUD_RATE_300, gurux_common.io.BaudRate.BAUD_RATE_600,
                gurux_common.io.BaudRate.BAUD_RATE_1800, gurux_common.io.BaudRate.BAUD_RATE_2400,
                gurux_common.io.BaudRate.BAUD_RATE_4800, gurux_common.io.BaudRate.BAUD_RATE_9600,
                gurux_common.io.BaudRate.BAUD_RATE_19200, gurux_common.io.BaudRate.BAUD_RATE_38400)

    def send(self, data, receiver=None):
        if not self.__h:
            raise Exception("Serial port is not open.")
        if self.__trace == TraceLevel.VERBOSE:
            self.__notifyTrace(TraceEventArgs(TraceTypes.SENT, data))

        #Reset last position if end of packet is used.
        with self.__syncBase.getSync():
            self.__syncBase.resetLastPosition()

        if not isinstance(data, bytes):
            data = bytes(_GXSynchronousMediaBase.toBytes(data))
        self.__h.write(data)
        self.__bytesSent += len(data)

    def __notifyMediaStateChange(self, state):
        ###Notify client from media state change.
        for it in self.__listeners:
            if self.__trace & TraceLevel.ERROR != 0:
                it.onTrace(self, TraceEventArgs(TraceTypes.INFO, state))
            it.onMediaStateChange(self, MediaStateEventArgs(state))

    #Handle received data.
    def __handleReceivedData(self, buff, info):
        self.__bytesReceived += len(buff)
        totalCount = 0
        if self.getIsSynchronous():
            arg = None
            with self.__syncBase.getSync():
                self.__syncBase.appendData(buff, 0, len(buff))
                #Search end of packet if it is given.
                if self.eop:
                    tmp = _GXSynchronousMediaBase.toBytes(self.eop)
                    totalCount = _GXSynchronousMediaBase.indexOf(buff, tmp, 0, len(buff))
                    if totalCount != -1:
                        if self.trace == TraceLevel.VERBOSE:
                            arg = TraceEventArgs(TraceTypes.RECEIVED, buff, 0, totalCount + 1)
                        self.__syncBase.setReceived()
            if arg:
                self.__notifyTrace(arg)
        else:
            self.__syncBase.resetReceivedSize()
            if self.trace == TraceLevel.VERBOSE:
                self.__notifyTrace(TraceEventArgs(TraceTypes.RECEIVED, buff))
            e = ReceiveEventArgs(buff, info)
            self.__notifyReceived(e)

    def __readThread(self):
        #pylint: disable=broad-except, bare-except
        while not self.__closing.isSet():
            try:
                data = self.__h.read()
                if data is not None:
                    self.__handleReceivedData(data, self.__portName)
                    #Give some time before read next bytes.  In this way we are
                    #not reading data one byte at the time.
                    time.sleep(0.1)
            except Exception:
                if not self.__closing.isSet():
                    traceback.print_exc()

    def open(self):
        self.close()
        if not self.__portName:
            raise Exception("Serial port is not selected.")

        with self.__syncBase.getSync():
            self.__syncBase.resetLastPosition()

        self.__notifyMediaStateChange(MediaState.OPENING)
        if self.__trace & TraceLevel.INFO != 0:
            eopString = str(self.eop)
            self.__notifyTrace(TraceEventArgs(TraceTypes.INFO,\
                "Settings: Port: " + self.__portName + " Baud Rate: " + str(self.baudRate) + \
                " Data Bits: " + str(int(self.dataBits)) + " Parity: " + str(self.parity) + \
               " Stop Bits: " + str(self.stopBits) + " Eop:" + eopString))

        self.__h.open(self.__portName)
        self.__closing.clear()
        self.rtsEnable = True
        self.dtrEnable = True
        self.__notifyMediaStateChange(MediaState.OPEN)
        self.__receiver = threading.Thread(target=self.__readThread)
        self.__receiver.start()

    def close(self):
        if self.__receiver:
            self.__closing.set()
            self.__notifyMediaStateChange(MediaState.CLOSING)
            self.__h.close()
            if self.__receiver:
                self.__receiver.join()
                self.__receiver = None
            self.__notifyMediaStateChange(MediaState.CLOSED)
            self.__bytesSent = 0
            self.__syncBase.resetReceivedSize()

    def __getBaudRate(self):
        if self.__h.isOpen():
            self.__h.baudRate = gurux_common.io.BaudRate(self.__h.getBaudRate())
        return self.__h.baudRate

    def __setBaudRate(self, value):
        if self.__h.baudRate != value:
            self.__h.baudRate = value
            if self.__h.isOpen():
                self.__h.setBaudRate(int(value))
            self.__notifyPropertyChanged("baudRate")

    baudRate = property(__getBaudRate, __setBaudRate)
    """baud rate."""

    def setBreakState(self, value):
        """Set break state."""
        self.__h.setBreakState(value)

    def getBytesToRead(self):
        """Gets the number of bytes in the receive buffer."""
        return self.__h.getBytesToRead()

    def getBytesToWrite(self):
        """Gets the number of bytes in the send buffer."""
        return self.__h.getBytesToWrite()

    def getCDHolding(self):
        """Gets the state of the Carrier Detect line for the port."""
        return self.__h.getCDHolding()

    def getCtsHolding(self):
        """Gets the state of the Clear-to-Send line."""
        return self.__h.getCtsHolding()

    def __getDataBits(self):
        if self.__h.isOpen():
            self.__h.dataBits = self.__h.getDataBits()
        return self.__h.dataBits

    def __setDataBits(self, value):
        self.__h.dataBits = value
        if self.__h.isOpen():
            self.__h.setDataBits(int(value))

    dataBits = property(__getDataBits, __setDataBits)
    """The standard length of data bits per byte."""

    def getDsrHolding(self):
        """"Gets the state of the Data Set Ready (DSR) signal."""
        return self.__h.getDsrHolding()

    def __getDtrEnable(self):
        return self.__h.getDtrEnable()

    def __setDtrEnable(self, value):
        self.__h.setDtrEnable(value)

    dtrEnable = property(__getDtrEnable, __setDtrEnable)
    """Is Data Terminal Ready (DTR) signal enabled."""

    def __getHandshake(self):
        if self.__h.isOpen():
            self.__handshake = self.__h.getHandshake()
        return self.__handshake

    def __setHandshake(self, value):
        self.__handshake = value

    handshake = property(__getHandshake, __setHandshake)
    """Handshaking protocol for serial port transmission of data."""

    def isOpen(self):
        return self.__h and self.__h.isOpen()

    def __getParity(self):
        if self.__h.isOpen():
            self.__h.parity = gurux_common.io.Parity(self.__h.getParity())
        return self.__h.parity

    def __setParity(self, value):
        self.__h.parity = value
        if self.__h.isOpen():
            self.__h.setParity(int(self.__h.parity))

    parity = property(__getParity, __setParity)
    """Parity-checking protocol."""

    def __getPortName(self):
        return self.__portName

    def __setPortName(self, value):
        if value != self.__portName:
            self.__portName = value
            self.__notifyPropertyChanged("port")

    port = property(__getPortName, __setPortName)
    """The port for communications, including but not limited to all available COM ports."""

    def __getRtsEnable(self):
        return self.__rtsEnable

    def __setRtsEnable(self, value):
        self.__rtsEnable = value

    rtsEnable = property(__getRtsEnable, __setRtsEnable)
    """Is Request to Send (RTS) signal enabled during serial communication."""

    def __getStopBits(self):
        if self.__h.isOpen():
            self.__h.stopBits = gurux_common.io.StopBits(self.__h.getStopBits())
        return self.__h.stopBits

    def __setStopBits(self, value):
        self.__h.stopBits = value
        if self.__h.isOpen():
            self.__h.setStopBits(int(self.__h.stopBits))

    stopBits = property(__getStopBits, __setStopBits)
    """Sets the standard number of stop bits per byte."""

    def receive(self, args):
        return self.__syncBase.receive(args)

    def getBytesSent(self):
        """Sent byte count."""
        return self.__bytesSent

    def getBytesReceived(self):
        """Received byte count."""
        return self.__bytesReceived

    def resetByteCounters(self):
        """Resets BytesReceived and BytesSent counters."""
        self.__bytesSent = 0
        self.__bytesReceived = 0

    def getSettings(self):
        """Media settings as a XML string."""
        sb = ""
        nl = "\r\n"
        if self.__portName:
            sb += "<Port>"
            sb += self.__portName
            sb += "</Port>"
            sb += nl

        if self.__h.baudRate != gurux_common.io.BaudRate.BAUD_RATE_9600:
            sb += "<BaudRate>"
            sb += str(int(self.__h.baudRate))
            sb += "</BaudRate>"
            sb += nl

        if self.__h.stopBits != gurux_common.io.StopBits.ONE:
            sb += "<StopBits>"
            sb += str(int(self.__h.stopBits))
            sb += "</StopBits>"
            sb += nl

        if self.__h.parity != gurux_common.io.Parity.NONE:
            sb += "<Parity>"
            sb += str(int(self.__h.parity))
            sb += "</Parity>"
            sb += nl

        if self.__h.dataBits != 8:
            sb += "<DataBits>"
            sb += str(int(self.__h.dataBits))
            sb += "</DataBits>"
            sb += nl
        return sb

    def setSettings(self, value):
        #Reset to default values.
        self.__portName = ""
        self.__h.baudRate = gurux_common.io.BaudRate.BAUD_RATE_9600
        self.__h.stopBits = gurux_common.io.StopBits.ONE
        self.__h.parity = gurux_common.io.Parity.NONE
        self.__h.dataBits = 8

    def copy(self, target):
        self.__portName = target.portName
        self.__h.baudRate = target.baudRate
        self.__h.stopBits = target.stopBits
        self.__h.parity = target.parity
        self.__h.dataBits = target.dataBits

    def getName(self):
        return self.__portName

    def getMediaType(self):
        return "Serial"

    def getSynchronous(self):
        return self.__lock

    #pylint: disable=no-member
    def getIsSynchronous(self):
        return self.__lock.locked()

    def resetSynchronousBuffer(self):
        with self.__syncBase.getSync():
            self.__syncBase.resetReceivedSize()

    def validate(self):
        if not self.__portName:
            raise Exception("Invalid port name.")

    def __getEop(self):
        return self.__eop

    def __setEop(self, value):
        self.__eop = value

    eop = property(__getEop, __setEop)

    def getReceiveDelay(self):
        return self.__receiveDelay

    def setReceiveDelay(self, value):
        self.__receiveDelay = value

    def getAsyncWaitTime(self):
        return self.__asyncWaitTime

    def setAsyncWaitTime(self, value):
        self.__asyncWaitTime = value

    def __str__(self):
        return self.__portName + ":" + str(int(self.__h.baudRate)) + " " +\
            str(self.__h.dataBits) + str(self.__h.parity.name) + str(int(self.__h.stopBits) + 1)
