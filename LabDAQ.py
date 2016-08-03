"""
LabDAQ.py ties together:
- UI elements
- data handler (deque type)
- matplotlib plotter
- serial device handler
"""
# Default values
POLL_RATE_ms = 250

#Interior dependencies
import sys
import serialHandler as sH
import dataHandler as dH
import plotHandler as pH
from dataDeque.dataDeque import dataDeque as dD
from serialControllers.arduino import Arduino as arduino


# Python 3
# import tkinter as tk
# from tkinter import ttk
# import _thread as thread

# Python 2
import Tkinter as tk
import ttk
import thread

#Python 2 and 3
import threading



class LabDAQ(tk.Frame): #, sH.SerialHandler, dH.DataHandler, pH.PlotHandler):
    def __init__(self, parent = None, *args, **kwargs):
        # Initialize TkInter frame and define parent
        tk.Frame.__init__(self, parent )
        self.parent = parent

        # Create arduino device and dataqueue as object parameters
        self.device = arduino()
        self.dataDeque = dD()

        # Create serial port frame, data handling frame, and plot frame
        self.sH = sH.SerialHandler( parent = parent, device = self.device )
        self.dH = dH.DataHandler( parent = parent, dataDeque = self.dataDeque )
        self.pH = pH.PlotHandler( parent = parent, dataDeque = self.dataDeque )

        # place into UI
        self.sH.grid(row=0, column=0, columnspan=6)
        self.dH.grid(row=1, column=0, columnspan=6)
        self.pH.grid(row=2, column=0, columnspan=6)

        # create poll rate menu
        self.create_poll_rate_menu()

        # generate quit button
        tk.Button(master=self.parent, text='Quit', command=self._quit).grid(row=4, column=2, columnspan=2)

        # start updating that data
        self.update_frequency = POLL_RATE_ms
        self.update_data()

    def update_data(self):
        # call this function again after {self.update_frequency time} (in ms)
        self.parent.after(self.update_frequency, self.update_data)
        #print "testing %s" % self.update_frequency

        #if device is connected,
        if self.device.is_connected():
            dataRow, dataFlag = self.device.poll() #read in data
            if dataFlag:
                self.dataDeque.append_data( dataRow ) #send to datadeque
                self.pH.update_plots( self.dataDeque ) #update the plot
        else:
            pass


    def create_poll_rate_menu(self):
        # change polling rate option
        tk.Label(self.parent, text="Choose Polling Rate:").grid(row=3, column=0)
        self.pollRateTk=tk.DoubleVar()
        pollRateOptions = [ 0.25, 0.5, 1.0, 5.0, 10.0, 30.0, 60.0]
        #create option menu and place into UI
        menu=tk.OptionMenu(self.parent, self.pollRateTk, *pollRateOptions)
        self.pollRateTk.set( str(POLL_RATE_ms/1000.) )
        menu.grid(row=3, column=1,columnspan=2)
        # label for units
        tk.Label(self.parent, text="ms/sample").grid(row=3, column=3)
        # create button to update poll rate
        tk.Button(self.parent, text='Update Polling Rate', state=tk.NORMAL,
                command=self.update_poll_rate).grid(row=3,column=4)


    def update_poll_rate(self):
        new_rate = float(self.pollRateTk.get()) * 1000
        self.update_frequency = int(new_rate)


    def _quit(self):
        self.device.disconnect()
        self.parent.quit()
        self.parent.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    LabDAQ(root).grid(column=0, row=0)
    root.mainloop()


'''
note: probably need one more class for actual handling of the connection between arduino and data queue, which would be thread handler too
        # Start new thread and call a 'portRead()' function that starts
        # reading data and putting in the queue
        self.readFlag = True
        thread.start_new_thread(self.portRead, ())

removed gui packing:
        portFrame = tk.LabelFrame(root, )
        portFrame.grid(row=0, column=0, padx=10)

        gui = spfThermo(portFrame)
        gui.grid(row=0, column=0)

        ttk.Separator(portFrame, orient=tk.VERTICAL).grid(row=0, column=1,
                                                      rowspan=4,
                                                      sticky='news',
                                                      padx=10, pady=10)

        gui2 = spfThermo(portFrame)
        gui2.grid(row=0, column=2, padx=10)

'''
