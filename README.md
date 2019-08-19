See An [Gurux](http://www.gurux.org/ "Gurux") for an overview.

Join the Gurux Community or follow [@Gurux](https://twitter.com/guruxorg "@Gurux") for project updates.

With gurux.serial component you can send data easily syncronously or asyncronously using serial port connection.

Open Source GXNet media component, made by Gurux Ltd, is a part of GXMedias set of media components, which programming interfaces help you implement communication by chosen connection type. Gurux media components also support the following connection types: serial port.

For more info check out [Gurux](http://www.gurux.org/ "Gurux").

We are updating documentation on Gurux web page. 

If you have problems you can ask your questions in Gurux [Forum](http://www.gurux.org/forum).

You can get source codes from http://www.github.com/gurux or intall package: 

```python
pip install gurux-common
pip install gurux-serial
```

Simple example
=========================== 
Before use you must set following settings:
* PortName
* BaudRate
* DataBits
* Parity
* StopBits

It is also good to add listener to listen following events.
* onError
* onReceived
* onMediaStateChange
* onTrace
* onPropertyChanged

This example sends data to the serial port and waits reply.
Change serial port before use.


```python
import time
from gurux_common import ReceiveParameters
from gurux_common import IGXMediaListener
from gurux_common.enums.TraceLevel import TraceLevel
from gurux_serial import GXSerial

#pylint: disable=no-self-argument
class sampleclient(IGXMediaListener):

    def __init__(self):
        #List available serial ports.
        print("Available ports:")
        print(str(GXSerial.getPortNames()))
        #Define End Of Packet char.
        eop = '\r'
        #TODO: Update correct port and serial port settings.
        media = GXSerial("SERIAL PORT TO USE")
        #Start to listen events from the media.
        media.addListener(self)
        #Show all traces.
        media.trace = TraceLevel.VERBOSE
        #Set EOP for the media.
        media.eop = eop
        try:
            #Open the connection.
            media.open()
            r = ReceiveParameters()
            r.eop = eop
            #Minimium amount of bytes to receive.
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
            media.send("Notify from the meter!\r")
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
```

