from gurux_common import ReceiveParameters
from gurux_serial import GXSerial
s = GXSerial("COM4")
s.eop = 13
s.open()
print(str(s.baudRate))
print(str(s.dataBits))
print(str(s.parity))
print(str(s.stopBits))
r = ReceiveParameters()
r.eop = 13
#r.count = 5
r.waitTime = 2000
with s.getSynchronous():
    s.send("Mikko\r\n")
    ret = s.receive(r)
    print(str(ret))
s.close()
print("Exit")
