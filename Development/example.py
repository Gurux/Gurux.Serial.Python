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
import time
from gurux_common import ReceiveParameters
from gurux_common import IGXMediaListener
from gurux_common.enums.TraceLevel import TraceLevel
from gurux_serial import GXSerial
# ---------------------------------------------------------------------------
# This example sends data to the serial port and waits reply.
# ---------------------------------------------------------------------------
#pylint: disable=no-self-argument
class sampleclient(IGXMediaListener):

    def __init__(self):
        #List available serial ports.
        print("Available ports:")
        print(str(GXSerial.getPortNames()))
        #Define End Of Packet char.
        eop = '\r'
        #Make connection using serial port.
        media = GXSerial("COM10")
        print(str(media))
        #Start to listen events from the media.
        media.addListener(self)
        #Update port here to call onPropertyChanged event.
        #TODO: Update correct port.
        media.port = "UPDATE CORRECT PORT"
        #Show all traces.
        media.trace = TraceLevel.VERBOSE
        #Set EOP for the media.
        media.eop = eop
        try:
            #Open the connection.
            media.open()
            r = ReceiveParameters()
            r.eop = eop
            r.count = 5
            #Wait reply for 2 seconds.
            r.waitTime = 2000
            ############################
            #Send data synchronously.
            with media.getSynchronous():
                media.send("Hello world!")
                #Send EOP
                media.send('\r')
                ret = media.receive(r)
                if ret:
                    print(str(r.reply.decode("ascii")))
                else:
                    raise Exception("Failed to receive reply from the server.")
            ############################
            #Send async data.
            media.send("Server !\r")
            #Wait 1 second to receive reply from the server.
            time.sleep(1)
        except Exception as ex:
            print(ex)
        media.close()
        media.removeListener(self)

    def onError(self, sender, ex):
        """
        Represents the method that will handle the error event of a Gurux
        component.

        sender :  The source of the event.
        ex : An Exception object that contains the event data.
        """
        print("Error has occured. " + str(ex))

    def onReceived(self, sender, e):
        """Media component sends received data through this method.

        sender : The source of the event.
        e : Event arguments.
        """
        print("New data is received. " + str(e))

    def onMediaStateChange(self, sender, e):
        """Media component sends notification, when its state changes.
        sender : The source of the event.
        e : Event arguments.
        """
        print("Media state changed. " + str(e))

    def onTrace(self, sender, e):
        """Called when the Media is sending or receiving data.

        sender : The source of the event.
        e : Event arguments.
        """
        print("trace:" + str(e))

    def onPropertyChanged(self, sender, e):
        """
        Event is raised when a property is changed on a component.

        sender : The source of the event.
        e : Event arguments.
        """
        print("Property {!r} has hanged.".format(str(e)))

if __name__ == '__main__':
    sampleclient()
