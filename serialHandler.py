"""
The SerialPortFrame class sets up a GUI frame that allows the selection
of a desired serial port from a list of all available serial ports, provides
connect and disconnect buttons, as wells as a connection indicator.
Added button to refresh available ports.
self.device refers to an Arduino object that can be used for data polling/acquisition
"""

BAUD_RATE = 115200

from serialControllers.getSerial import getSerialPorts
from serialControllers.arduino import Arduino as arduino

# Python 3
# import tkinter as tk
# from tkinter import ttk

# Python 2
import Tkinter as tk
import ttk


class SerialHandler(tk.Frame):

    def __init__(self, parent=None, device=None, *args, **kwargs):
        #Initialize TkInter frame and define parent
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # variable for whether or not device is connected
        if device:
            self.device = device
        else:
            self.device = arduino()

        #generate UI elements
        self.create_serial_widgets(parent, "Instrument")


    # abstracted this to a separate function so it can be updated on-the-fly
    def check_for_ports(self):
        self.ports = getSerialPorts()
        #print self.ports


    def create_serial_widgets(self, parent, instrument):
        #prepare list of serial port options
        self.check_for_ports()
        # create label at top of frame
        tk.Label(self, text=instrument).grid(row=0, column=0, columnspan=3)
        # tag for the selector button for COM port
        tk.Label(self, text='COM Port:').grid(row=1, column=0, sticky='e')
        #generate options for COM ports to connect to
        self.create_connection_option_menu(parent)
        # create connect and disconnect buttons
        self.create_connection_buttons()
        #create indicator for connected/not connected
        self.create_connection_indicator()


    def create_connection_option_menu(self, parent):
        # create TkInter string variable type for currently selected menu item
        self.portsVar = tk.StringVar(parent)
        # set initial value
        self.portsVar.set('No port selected')

        # create options menu
        if not self.ports:        # there are no available COM ports
            self.optionsMenu = tk.OptionMenu(self, self.portsVar, self.portsVar.get())
        else:
            self.optionsMenu = tk.OptionMenu(self, self.portsVar, *self.ports)

        #place into UI
        self.optionsMenu.grid(row=1, column=1, columnspan=2, sticky='ew')


    def create_connection_buttons(self):
        #create connect and disconnect buttons, both disabled by default
        self.connectButton = tk.Button(self, text='Connect', state=tk.DISABLED, command=self.connect_arduino)
        self.disconnectButton = tk.Button(self, text='Disconnect', state=tk.DISABLED, command=self.disconnect_arduino)
        self.refreshButton = tk.Button(self, text='Refresh Ports', state=tk.NORMAL, command=self.update_option_menu)

        # place buttons into UI
        self.connectButton.grid(row=2, column=0)
        self.disconnectButton.grid(row=2, column=1)
        self.refreshButton.grid(row=1, column=4)

        # if ports are available, allow connect button to be enabled
        self.check_ports_availability()

    def check_ports_availability(self):
        # if there are available ports, allow connect button to be available
        if self.ports:
            self.connectButton.configure(state=tk.NORMAL)



    def create_connection_indicator(self):
        self.canvas = tk.Canvas(self, width=100, height=55)
        self.indicator = self.canvas.create_oval(20, 10, 60, 50,
                                                 outline='gray70',
                                                 fill='dark green',
                                                 width=5)
        self.canvas.grid(row=2, column=2)

    def connect_arduino(self):
        #report button action
        #print('Connect button clicked')

        #getting currently selected option from ports menu
        port = self.portsVar.get()

        #attempt to open connection; if successful, modify button availability/indicator
        try:
            self.device.connect_to_arduino(port, baud=BAUD_RATE)      # define self.device
            self.canvas.itemconfigure(self.indicator, fill='green')
            self.disconnectButton.configure(state=tk.NORMAL)
            self.connectButton.configure(state=tk.DISABLED)
            print "connected successfully to device on port %s" % port
        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print "failed to connect to arduino"


    def disconnect_arduino(self):
        #report button click
        #print('Disconnect button clicked')

        #attempt to disconnect and update buttons/indicators
        try:
            self.device.disconnect()
            self.canvas.itemconfigure(self.indicator, fill='dark green')
            self.disconnectButton.configure(state=tk.DISABLED)
            self.connectButton.configure(state=tk.NORMAL)
            print "closed connection successfully from port %s" % self.device.port
            self.isConnected = False
        #if unsuccessful, print failure notice
        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print "failed to disconnect from arduino"


    def update_option_menu(self):
        # set initial value
        self.portsVar.set('No port selected')

        # update port options
        self.check_for_ports()

        #clear current menu options
        self.optionsMenu['menu'].delete(0,'end')

        # create options menu
        for port in self.ports:
            self.optionsMenu['menu'].add_command( label=port, command=tk._setit(self.portsVar, port) )
            
        # if ports are available, allow connect button to be enabled
        self.check_ports_availability()

    #upon exit, disconnect from device and quit (if errors thrown, oh well!)
    def exit(self):
        self.device.disconnect()
        self.quit()


####
# FOR TESTING PURPOSES only
####

if __name__ == '__main__':
    root = tk.Tk()
    SerialHandler(root).pack(side="top", fill="both",expand=True)
    root.mainloop()
