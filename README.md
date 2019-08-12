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

and if in server mode following events might be important.
* onClientConnected
* onClientDisconnected                

```python
#Change name of the COM port to correct one.
cl = new GXSerial("COM1")
cl.baudRate = BAUD_RATE_9600
cl.dataBits = 8
cl.parity = Parity.None
cl.stopBits = StopBits.ONE
cl.open()
```

Data is send with send command:

```python
cl.send("Hello World!")
```
In default mode received data is coming as asynchronously from OnReceived event.
Event listener is added like this:
1. Ads class that you want to use to listen media events and derive class from IGXMediaListener.

```python
class GXNetListener(IGXMediaListener):
    """Media listener."""

    def onError(sender, ex):
        """
        Represents the method that will handle the error event of a Gurux component.

        sender : The source of the event.
        ex : An Exception object that contains the event data.
        """

    def onReceived(sender, e):
        """
        Media component sends received data through this method.

        sender : The source of the event.
        e : Event arguments.
        """
    
    def onMediaStateChange(sender, e):
        """
        Media component sends notification, when its state changes.

        sender : The source of the event.    
        e : Event arguments.
        """

    
    def onTrace(sender, e):
        """
        Called when the Media is sending or receiving data.

        sender : The source of the event.    
        e : Trace message.
        """
           
    def onPropertyChanged(sender, e):
        """
        Represents the method that will handle the System.ComponentModel.INotifyPropertyChanged.PropertyChanged
        event raised when a property is changed on a component.
    	sender : The source of the event.
    	e : A System.ComponentModel.PropertyChangedEventArgs that contains the event data.
        """    
```

Listener is registered calling addListener method.
```python
cl.addListener(self)

```

Data can be also send as syncronous if needed.

```python
with cl.getSynchronous():
    reply = ""
    p = ReceiveParameters()
    #End of Packet.
    p.eop = 0x10 
    #How long reply is waited.   
    p.waitTime = 1000
    cl.send("Hello World!")
    if not cl.receive(p):    
        raise Exception("Failed to receive response..")    

```
