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
import ctypes
import ctypes.wintypes
import threading
from .GXSettings import GXSettings
from .IGXNative import IGXNative

#Constant values.
INVALID_HANDLE_VALUE = -1
MS_DSR_ON = 32
EV_RING = 256
EV_PERR = 512
EV_ERR = 128
SETXOFF = 1
EV_RXCHAR = 1
OPEN_EXISTING = 3
FILE_ATTRIBUTE_NORMAL = 128
FILE_FLAG_OVERLAPPED = 1073741824
GENERIC_WRITE = 1073741824
GENERIC_READ = 2147483648
PURGE_TXABORT = 1
PURGE_RXABORT = 2
PURGE_TXCLEAR = 4
PURGE_RXCLEAR = 8

RTS_CONTROL_HANDSHAKE = 2
RTS_CONTROL_DISABLE = 0
RTS_CONTROL_ENABLE = 1
RTS_CONTROL_TOGGLE = 3

DTR_CONTROL_HANDSHAKE = 2
DTR_CONTROL_DISABLE = 0
DTR_CONTROL_ENABLE = 1
SETRTS = 3
CLRRTS = 4
SETDTR = 5
CLRDTR = 6
XON = 0x11
XOFF = 0x13
MS_RLSD_ON = 128
#Error code defs.
ERROR_SUCCESS = 0
ERROR_NOT_ENOUGH_MEMORY = 8
ERROR_OPERATION_ABORTED = 995
ERROR_IO_INCOMPLETE = 996
ERROR_IO_PENDING = 997
ERROR_INVALID_USER_BUFFER = 1784

#Error code defs.
ERROR_SUCCESS = 0
ERROR_NOT_ENOUGH_MEMORY = 8
ERROR_OPERATION_ABORTED = 995
ERROR_IO_INCOMPLETE = 996
ERROR_IO_PENDING = 997
ERROR_INVALID_USER_BUFFER = 1784

READ_CONTROL = 0x00020000
STANDARD_RIGHTS_READ = READ_CONTROL

KEY_QUERY_VALUE = 0x0001
HKEY_LOCAL_MACHINE = 0x80000002
SYNCHRONIZE = 0x00100000
KEY_ENUMERATE_SUB_KEYS = 0x0008
KEY_NOTIFY = 0x0010
KEY_READ = ((STANDARD_RIGHTS_READ | KEY_QUERY_VALUE | KEY_ENUMERATE_SUB_KEYS | KEY_NOTIFY) & (~SYNCHRONIZE))
KEY_EXECUTE = KEY_READ & ~SYNCHRONIZE

if ctypes.sizeof(ctypes.c_void_p) == 8:
    ULONG_PTR = ctypes.c_int64
else:
    ULONG_PTR = ctypes.c_ulong

#Structyres.
class DUMMYSTRUCTNAME(ctypes.Structure):
    # pylint: disable=too-few-public-methods
    _fields_ = [('Offset', ctypes.wintypes.DWORD),\
    ('OffsetHigh', ctypes.wintypes.DWORD),]

class DUMMYUNIONNAME(ctypes.Union):
    # pylint: disable=too-few-public-methods
    _fields_ = [('_0', DUMMYSTRUCTNAME),\
    ('Pointer', ctypes.c_void_p),]

class OVERLAPPED(ctypes.Structure):
    # pylint: disable=too-few-public-methods
    _fields_ = [('Internal', ULONG_PTR),\
    ('InternalHigh', ULONG_PTR),\
    ('_0', DUMMYUNIONNAME),\
    ('hEvent', ctypes.wintypes.HANDLE),]

class COMSTAT(ctypes.Structure):
    # pylint: disable=too-few-public-methods
    _fields_ = [('fCtsHold', ctypes.wintypes.DWORD, 1),\
    ('fDsrHold', ctypes.wintypes.DWORD, 1),\
    ('fRlsdHold', ctypes.wintypes.DWORD, 1),\
    ('fXoffHold', ctypes.wintypes.DWORD, 1),\
    ('fXoffSent', ctypes.wintypes.DWORD, 1),\
    ('fEof', ctypes.wintypes.DWORD, 1),\
    ('fTxim', ctypes.wintypes.DWORD, 1),\
    ('fReserved', ctypes.wintypes.DWORD, 25),\
    ('cbInQue', ctypes.wintypes.DWORD),\
    ('cbOutQue', ctypes.wintypes.DWORD),]

class DCB(ctypes.Structure):
    # pylint: disable=too-few-public-methods, too-many-instance-attributes
    _fields_ = [('DCBlength', ctypes.wintypes.DWORD),\
    ('BaudRate', ctypes.wintypes.DWORD),\
    ('fBinary', ctypes.wintypes.DWORD, 1),\
    ('fParity', ctypes.wintypes.DWORD, 1),\
    ('fOutxCtsFlow', ctypes.wintypes.DWORD, 1),\
    ('fOutxDsrFlow', ctypes.wintypes.DWORD, 1),\
    ('fDtrControl', ctypes.wintypes.DWORD, 2),\
    ('fDsrSensitivity', ctypes.wintypes.DWORD, 1),\
    ('fTXContinueOnXoff', ctypes.wintypes.DWORD, 1),\
    ('fOutX', ctypes.wintypes.DWORD, 1),\
    ('fInX', ctypes.wintypes.DWORD, 1),\
    ('fErrorChar', ctypes.wintypes.DWORD, 1),\
    ('fNull', ctypes.wintypes.DWORD, 1),\
    ('fRtsControl', ctypes.wintypes.DWORD, 2),\
    ('fAbortOnError', ctypes.wintypes.DWORD, 1),\
    ('fDummy2', ctypes.wintypes.DWORD, 17),\
    ('wReserved', ctypes.wintypes.WORD),\
    ('XonLim', ctypes.wintypes.WORD),\
    ('XoffLim', ctypes.wintypes.WORD),\
    ('ByteSize', ctypes.wintypes.BYTE),\
    ('Parity', ctypes.wintypes.BYTE),\
    ('StopBits', ctypes.wintypes.BYTE),\
    ('XonChar', ctypes.c_char),\
    ('XoffChar', ctypes.c_char),\
    ('ErrorChar', ctypes.c_char),\
    ('EofChar', ctypes.c_char),\
    ('EvtChar', ctypes.c_char),\
    ('wReserved1', ctypes.wintypes.WORD),]

#ctypes.windll.kernel32.WriteFile don't work for all Windows versions for some
#reason.
_stdcall_libraries = {}
_stdcall_libraries['kernel32'] = ctypes.WinDLL('kernel32')
WriteFile = _stdcall_libraries['kernel32'].WriteFile
WriteFile.restype = ctypes.wintypes.BOOL
LPOVERLAPPED = ctypes.POINTER(OVERLAPPED)
# pylint: disable=no-member

#LPDWORD is missing from older ctypes.wintypes.
LPDWORD = ctypes.POINTER(ctypes.wintypes.DWORD)

WriteFile.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.LPCVOID, ctypes.wintypes.DWORD, LPDWORD, LPOVERLAPPED]

# pylint: disable=too-many-public-methods,too-many-instance-attributes
class GXWindowsHandler(GXSettings, IGXNative):
    def __init__(self):
        """Constructor."""
        GXSettings.__init__(self)
        self.h = INVALID_HANDLE_VALUE
        self._overlapped_read = None
        self._overlapped_write = None
        self.__unicode = None
        self.__closed = threading.Event()
        if self.isUnicode():
            self._closing = ctypes.windll.Kernel32.CreateEventW(0, 0, 0, 0)
        else:
            self._closing = ctypes.windll.Kernel32.CreateEventA(0, 0, 0, 0)

    def __del__(self):
        """Destructor."""
        if self._closing != INVALID_HANDLE_VALUE:
            ctypes.windll.Kernel32.CloseHandle(self._closing)
            self._closing = INVALID_HANDLE_VALUE

    def isUnicode(self):
        ##Check is UNICODE or ASCII versions used.
        if self.__unicode is None:
            try:
                _stdcall_libraries['kernel32'].CreateEventW
                self.__unicode = True
            except AttributeError:
                self.__unicode = False
        return self.__unicode

    def getPortNames(self):
        """Returns available serial ports."""
        #Use RegOpenKeyEx() with the new Registry path to get an open handle
        #to the child key you want to enumerate.
        hKey = ctypes.wintypes.HKEY()
        if self.isUnicode():
            ret = ctypes.windll.Kernel32.RegOpenKeyExW(HKEY_LOCAL_MACHINE, "HARDWARE\\DEVICEMAP\\SERIALCOMM", \
                0, KEY_ENUMERATE_SUB_KEYS | KEY_EXECUTE | KEY_QUERY_VALUE, ctypes.byref(hKey))
        else:
            ret = ctypes.windll.Kernel32.RegOpenKeyExA(HKEY_LOCAL_MACHINE, "HARDWARE\\DEVICEMAP\\SERIALCOMM", \
                0, KEY_ENUMERATE_SUB_KEYS | KEY_EXECUTE | KEY_QUERY_VALUE, ctypes.byref(hKey))
        #If there are no serial ports installed.
        if ret == 2:
            return []
        if ret != 0:
            raise Exception('Failed to get port names: {!r}'.format(ctypes.WinError(ret)))

        dwType = ctypes.wintypes.DWORD()
        dwcValueName = ctypes.wintypes.DWORD(256)
        valueName = ctypes.create_unicode_buffer(256)
        cbData = ctypes.wintypes.DWORD(256)
        deviceName = ctypes.create_unicode_buffer(236)
        pos = 0
        ports = []
        while pos < 100:
            if self.isUnicode():
                ret = ctypes.windll.Kernel32.RegEnumValueW(hKey, pos, valueName, ctypes.byref(dwcValueName), None, ctypes.byref(dwType), deviceName, ctypes.byref(cbData))
            else:
                ret = ctypes.windll.Kernel32.RegEnumValueA(hKey, pos, valueName, ctypes.byref(dwcValueName), None, ctypes.byref(dwType), deviceName, ctypes.byref(cbData))
            if ret != 0:
                break
            ports.append(deviceName.value)
            pos += 1
        ctypes.windll.Kernel32.RegCloseKey(hKey)
        return ports

    def __getCommState(self):
        if self.h == INVALID_HANDLE_VALUE:
            raise Exception("Serial port is not open")
        ctypes.windll.Kernel32.SetCommMask(self.h, EV_ERR)
        # Get state
        dcb = DCB()
        if ctypes.windll.Kernel32.GetCommState(self.h, ctypes.byref(dcb)) == 0:
            raise Exception("Failed to get comm state.")
        return dcb

    def __updateSettings(self):
        """Set communication parameters."""
        # pylint: disable=attribute-defined-outside-init
        if self.h == INVALID_HANDLE_VALUE:
            raise Exception("Serial port is not open")

        dcb = self.__getCommState()
        dcb.BaudRate = self.baudRate
        dcb.ByteSize = self.dataBits
        dcb.Parity = self.parity
        # Disable Parity Check
        if dcb.Parity == 0:
            dcb.fParity = 0
        else:
            dcb.fParity = 1
        dcb.StopBits = self.stopBits
        dcb.fBinary = 1
        dcb.fNull = 0
        dcb.fErrorChar = 0
        dcb.fAbortOnError = 0
        dcb.XonChar = XON
        dcb.XoffChar = XOFF
        dcb.fRtsControl = RTS_CONTROL_DISABLE
        dcb.fDtrControl = DTR_CONTROL_DISABLE
        if not ctypes.windll.Kernel32.SetCommState(self.h, ctypes.byref(dcb)):
            raise Exception('Failed to set serial port settings: {!r}'.format(ctypes.WinError()))

    def open(self, port):
        #pylint: disable=bare-except
        """
        Open serial port.

        port: Name of serial port.
        """
        self.close()
        if not port:
            raise Exception("Invalid serial port name.")
        # Open the file for writing.
        if self.isUnicode():
            self.h = ctypes.windll.Kernel32.CreateFileW('\\\\.\\' + port, GENERIC_READ | GENERIC_WRITE,
                                                        0,  # exclusive access
                                                        None,  # no security
                                                        OPEN_EXISTING,
                                                        FILE_FLAG_OVERLAPPED,
                                                        0)
        else:
            self.h = ctypes.windll.Kernel32.CreateFileA('\\\\.\\' + port, GENERIC_READ | GENERIC_WRITE,
                                                        0,  # exclusive access
                                                        None,  # no security
                                                        OPEN_EXISTING,
                                                        FILE_FLAG_OVERLAPPED,
                                                        0)

        if self.h == INVALID_HANDLE_VALUE:
            ret = ctypes.windll.Kernel32.GetLastError()
            raise Exception("Failed to open port {!r}: {!r}".format(port, str(ctypes.WinError(ret))))
        try:
            if self.isUnicode():
                self._overlapped_read = OVERLAPPED(hEvent=ctypes.windll.Kernel32.CreateEventW(0, 0, 0, 0))
                self._overlapped_write = OVERLAPPED(hEvent=ctypes.windll.Kernel32.CreateEventW(0, 0, 0, 0))
            else:
                self._overlapped_read = OVERLAPPED(hEvent=ctypes.windll.Kernel32.CreateEventA(0, 0, 0, 0))
                self._overlapped_write = OVERLAPPED(hEvent=ctypes.windll.Kernel32.CreateEventA(0, 0, 0, 0))
            if ctypes.windll.Kernel32.ResetEvent(self._closing) == 0:
                ret = ctypes.windll.Kernel32.GetLastError()
                raise Exception("Failed to open port {!r}: {!r}".format(port, str(ctypes.WinError(ret))))
            self.__updateSettings()
            #Clear buffers.
            ctypes.windll.Kernel32.PurgeComm(self.h, PURGE_TXCLEAR | PURGE_TXABORT | PURGE_RXCLEAR | PURGE_RXABORT)
        except Exception as e:
            try:
                self.close()
            except:
                pass
            raise e

    def isOpen(self):
        return self.h != INVALID_HANDLE_VALUE

    def close(self):
        """
        Close serial port.
        """
        if self.h != INVALID_HANDLE_VALUE:
            ctypes.windll.Kernel32.SetEvent(self._closing)
            self.__closed.wait()
            if self._overlapped_read:
                ctypes.windll.Kernel32.CloseHandle(self._overlapped_read.hEvent)
                self._overlapped_read = None
            if self._overlapped_write:
                ctypes.windll.Kernel32.CloseHandle(self._overlapped_write.hEvent)
                self._overlapped_write = None
            ctypes.windll.Kernel32.CloseHandle(self.h)
            self.h = INVALID_HANDLE_VALUE

    def getBaudRate(self):
        """
        Get baud rate.
        """
        return self.__getCommState().BaudRate


    def setBaudRate(self, value):
        """
        Set baud rate.
        """
        self.__updateSettings()


    def getDataBits(self):
        """Get data bits.
        """
        return self.__getCommState().ByteSize


    def setDataBits(self, value):
        """Set amount of data bits.
        value : Amount of data bits.
        """
        self.__updateSettings()


    def getParity(self):
        """Get parity.
        """
        return self.__getCommState().fParity

    def setParity(self, value):
        """
        Set parity.
        value : parity.
        """
        self.__updateSettings()


    def getStopBits(self):
        """
        Get stop bits.
        """
        return self.__getCommState().StopBits


    def setStopBits(self, value):
        """
        Set stop bits.
        value: Amount of stop bits.
        """
        self.__updateSettings()

    def setBreakState(self, value):
        """
        Set break state.
        value : Is serial port in break state.
        """
        if value:
            if ctypes.windll.Kernel32.SetCommBreak(self.h) == 0:
                raise Exception("setBreakState failed ({!r})".format(ctypes.WinError()))
        else:
            if ctypes.windll.Kernel32.ClearCommBreak(self.h) == 0:
                raise Exception("setBreakState failed ({!r})".format(ctypes.WinError()))

    def getRtsEnable(self):
        """
        Get Request To Send state.
        """
        dcb = self.__getCommState()
        return dcb.fRtsControl == RTS_CONTROL_ENABLE

    def setRtsEnable(self, value):
        """Set Request To Send state.
        value: Is RTS set.
        """
        if value:
            tmp = ctypes.wintypes.DWORD(SETRTS)
        else:
            tmp = ctypes.wintypes.DWORD(CLRRTS)
        if ctypes.windll.Kernel32.EscapeCommFunction(self.h, tmp) == 0:
            raise Exception("setRtsEnable failed ({!r})".format(ctypes.WinError()))

    def getDtrEnable(self):
        """
        Is Data Terminal ready set.
        """
        dcb = self.__getCommState()
        return dcb.fDtrControl == DTR_CONTROL_ENABLE

    def setDtrEnable(self, value):
        """Is Data Terminal ready set.
        value : True, if DTR is set.
        """
        if value:
            tmp = ctypes.wintypes.DWORD(SETDTR)
        else:
            tmp = ctypes.wintypes.DWORD(CLRDTR)
        if ctypes.windll.Kernel32.EscapeCommFunction(self.h, tmp) == 0:
            raise Exception("Read failed ({!r})".format(ctypes.WinError()))

    def getDsrHolding(self):
        """
        Get Get Data Set Ready holding flag.
        """
        flags = ctypes.wintypes.DWORD()
        comstat = COMSTAT()
        if not ctypes.windll.Kernel32.ClearCommError(self.h, ctypes.byref(flags), ctypes.byref(comstat)):
            raise Exception("ClearCommError failed ({!r})".format(ctypes.WinError()))
        return comstat.fDsrHold != 0

    def getBytesToRead(self):
        """
        Returns amount of bytes to read.
        """
        flags = ctypes.wintypes.DWORD()
        comstat = COMSTAT()
        if not ctypes.windll.Kernel32.ClearCommError(self.h, ctypes.byref(flags), ctypes.byref(comstat)):
            raise Exception("ClearCommError failed ({!r})".format(ctypes.WinError()))
        return comstat.cbInQue

    def getBytesToWrite(self):
        """
        Returns amount of bytes to write.
        """
        flags = ctypes.wintypes.DWORD()
        comstat = COMSTAT()
        if not ctypes.windll.ClearCommError(self.h, ctypes.byref(flags), ctypes.byref(comstat)):
            raise Exception("ClearCommError failed ({!r})".format(ctypes.WinError()))
        return comstat.cbOutQue

    def read(self):
        """Read data from serial port to the buffer."""
        if self.h == INVALID_HANDLE_VALUE:
            raise Exception("Serial port is not open")
        count = self.getBytesToRead()
        if count == 0:
            count = 1
        buf = ctypes.create_string_buffer(count)
        c = ctypes.wintypes.DWORD()
        if ctypes.windll.Kernel32.ReadFile(self.h, buf, count, ctypes.byref(c), ctypes.byref(self._overlapped_read)) == 0:
            ret = ctypes.windll.Kernel32.GetLastError()
            if ret not in (ERROR_SUCCESS, ERROR_IO_PENDING):
                raise Exception("Read failed ({!r})".format(ctypes.WinError()))
            arrtype = ctypes.wintypes.HANDLE * 2
            handle_array = arrtype(self._closing, self._overlapped_read.hEvent)
            ret = ctypes.windll.kernel32.WaitForMultipleObjects(2, handle_array, 0, -1)
            #If user has close the media.
            if ret == 0:
                self.__closed.set()
                return None

            if ctypes.windll.Kernel32.GetOverlappedResult(self.h, ctypes.byref(self._overlapped_read), ctypes.byref(c), True) == 0:
                if ctypes.windll.Kernel32.GetLastError() != ERROR_OPERATION_ABORTED:
                    raise Exception("Read failed  ({!r})".format(ctypes.WinError()))
        return bytearray(buf.raw[:c.value])

    def write(self, data):
        """Write data to the serial port."""
        if self.h == INVALID_HANDLE_VALUE:
            raise Exception("Serial port is not open")
        n = ctypes.wintypes.DWORD()
        if WriteFile(self.h, data, len(data), ctypes.byref(n), self._overlapped_write) == 0:
            errorcode = ERROR_SUCCESS
        else:
            errorcode = ctypes.windll.Kernel32.GetLastError()
        if errorcode in (ERROR_INVALID_USER_BUFFER, ERROR_NOT_ENOUGH_MEMORY, ERROR_OPERATION_ABORTED):
            return 0
        if errorcode == ERROR_IO_PENDING:
            arrtype = ctypes.wintypes.HANDLE * 2
            handle_array = arrtype(self._closing, self._overlapped_write.hEvent)
            ret = ctypes.windll.kernel32.WaitForMultipleObjects(2, handle_array, 0, 1000)
            #If user has close the media.
            if ret == 0:
                return None
        if errorcode == ERROR_SUCCESS:
            return len(data)
        raise Exception("write failed ({!r})".format(ctypes.WinError()))

    def getCtsHolding(self):
        """Returns Clear To Send holding flag."""
        flags = ctypes.wintypes.DWORD()
        comstat = COMSTAT()
        if not ctypes.windll.Kernel32.ClearCommError(self.h, ctypes.byref(flags), ctypes.byref(comstat)):
            raise Exception("ClearCommError failed ({!r})".format(ctypes.WinError()))
        return comstat.fCtsHold != 0

    def getCDHolding(self):
        """Gets the state of the Carrier Detect line for the port."""
        status = ctypes.wintypes.DWORD()
        if ctypes.windll.Kernel32.GetCommModemStatus(self.h, status) == 0:
            raise Exception("ClearCommError failed ({!r})".format(ctypes.WinError()))
        return (status & MS_RLSD_ON) != 0

    def getHandshake(self):
        """Gets the handshaking protocol for serial port transmission of data."""
        dcb = self.__getCommState()
        #Disable DTR monitoring
        #Disable RTS (Ready To Send)
        if dcb.fDtrControl == DTR_CONTROL_DISABLE and dcb.fRtsControl == RTS_CONTROL_DISABLE:
            #Enable XON/XOFF for transmission
            #Enable XON/XOFF for receiving
            if dcb.fOutX and dcb.fInX:
                #XOnXOff
                return 1
            #None
            return 0
        #Enable XON/XOFF for transmission
        #Enable XON/XOFF for receiving
        if dcb.fOutX and dcb.fInX:
            #RequestToSendXOnXOff
            return 3
        #hardware flow control is used.
        return 2

    def setHandshake(self, value):
        # pylint: disable=attribute-defined-outside-init
        """Sets the handshaking protocol for serial port transmission of data."""
        dcb = self.__getCommState()
        #None
        if value == 0:
            dcb.fDtrControl = DTR_CONTROL_DISABLE
            #Disable RTS (Ready To Send)
            dcb.fRtsControl = RTS_CONTROL_DISABLE
            dcb.fOutX = dcb.fInX = 0
        #XOnXOff
        elif value == 1:
            dcb.fDtrControl = DTR_CONTROL_DISABLE
            #Disable RTS (Ready To Send)
            dcb.fRtsControl = RTS_CONTROL_DISABLE
            dcb.fOutX = dcb.fInX = 1
        #hardware flow control is used.
        elif value == 2:
            dcb.fDtrControl = DTR_CONTROL_ENABLE
            #Disable RTS (Ready To Send)
            dcb.fRtsControl = RTS_CONTROL_ENABLE
            dcb.fOutX = dcb.fInX = 0
        #RequestToSendXOnXOff
        elif value == 3:
            dcb.fDtrControl = DTR_CONTROL_ENABLE
            #Disable RTS (Ready To Send)
            dcb.fRtsControl = RTS_CONTROL_ENABLE
            dcb.fOutX = dcb.fInX = 1
        if ctypes.windll.Kernel32.SetCommState(self.h, ctypes.byref(dcb)) == 0:
            raise Exception("Failed to set comm state.")
