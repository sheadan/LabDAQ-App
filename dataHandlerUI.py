"""
The data handler is a TkInter gui for:
- toggle data saving on/off
- select file name/location
"""

import datahandler

import os

# Python 3
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


class DataHandlerUI(tk.Frame):

    def __init__(self, parent=None, dataHandler=None, *args, **kwargs):
        #Initialize TkInter frame and define parent
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # initialize  data handler
        if not dataHandler:
            self.DataHandler = dataDeque.datahandler.DataHandler()
        else:
            self.DataHandler = dataHandler

        #generate UI elements
        self.create_filename_selector()
        self.create_recording_checkbox()
        self.create_alarm_config_button()


    def create_filename_selector(self):
        """create filename selector to choose where to save data"""
        # label for the filename location tk variable
        self.filename = tk.StringVar()
        self.update_record_file_name( self.DataHandler.recordFilename )
        # place labels into UI
        tk.Label(self, text='Save to:').grid(row=1, column=0, sticky='e')
        tk.Label(self, textvariable=self.filename).grid(row=1, column=1, columnspan=2)
        # button for choosing file name, placed into UI
        tk.Button(self, text='Select...', command=self.ask_filename).grid(row=1, column=3)


    def create_recording_checkbox(self):
        """UI checkbox and label for recording data to file"""
        # create Tk boolean variable
        self.recordBool=tk.BooleanVar()
        self.recordBool.set( self.DataHandler.recordFlag )
        #Check button, and packing
        tk.Checkbutton(self, text="Record data to file?",
                variable=self.recordBool, command=self.update_record_flag,
                onvalue=1, offvalue=0).grid(row=2, column=0, columnspan=3)


    def create_alarm_config_button(self):
        """UI button to prompt alarm configuration"""
        #Check button, and packing
        tk.Button(self, text='Configure Alarms', command=self.config_alarms).grid(row=3, column=1, columnspan=2)


    def ask_filename(self):
        """File dialog for choosing file save location"""
        # settings for file dialog
        options = {
            'defaultextension' : '.txt',
            'filetypes' : [('all files', '.*'), ('text files', '.txt')],
            'initialdir' : self.filename.get(),
            'initialfile' : 'myfile.txt',
            'parent' : self.parent,
            'title' : 'This is a title'
        }
        # get filename
        fn = filedialog.asksaveasfilename(**options)
        self.update_record_file_name( fn )


    def update_record_flag(self):
        """Update current value of recording flag"""
        #get current value of the recording Boolean
        curVal= self.recordBool.get()
        # attempt to change the flag. the function returns a Boolean
        # which indicates cuccess/failure in changing flag
        if self.DataHandler.set_recording_flag( curVal ):
            return
        else:
            opposite = not curVal
            self.recordBool.set(opposite)


    def update_record_file_name(self, fn):
        """Update the save file name/location"""
        self.DataHandler.set_recording_file_name( fn )
        self.filename.set(fn)


    def config_alarms(self):
        """Configure alarms for channels"""
        # create popup box
        toplevel = tk.Toplevel()

        # Label for checkbuttons
        tk.Label( toplevel, text="Set alarm").grid(row=0, column=0, columnspan=2)
        tk.Label( toplevel, text="Trigger Voltage (V)").grid(row=0, column=2, columnspan=2)

        # initialize arrays for trigger values and booleans (whether or not a channel has an alarm)
        trigVals = []
        boolVals = []

        # iterate through to set the alarms that you want set!
        def set_alarm():
            for index,boolVal in enumerate(boolVals):
                if boolVal.get() == 1:
                    valueToWatch = float(trigVals[index].get())
                    self.DataHandler.channels[index].set_alarm( valueToWatch )
                else:
                    self.DataHandler.channels[index].alarm = None
            update_UI()


        def update_UI():# create UI, appropriately set UI components
            for index,channel in enumerate(self.DataHandler.channels):
                # If channel has an alarm, show it
                if channel.alarm:
                    trigVals[index].set( channel.alarm.triggerValue )
                else:
                    trigVals[index].set(0)

        def initialize_UI():
            #Initialize double variable for trigger and boolean for set/not set status
            for index,channel in enumerate(self.DataHandler.channels):
                txt = "Channel A%s" % (index)
                boolVals.append( tk.IntVar() )
                chk = tk.Checkbutton( toplevel, text=txt,
                                command = set_alarm,
                                variable = boolVals[index],
                                onvalue=1, offvalue=0 )
                chk.grid(row=index+1, column=0, columnspan=2)
                scale = tk.Scale( toplevel, from_=0.0, to=5.0,
                                        orient=tk.HORIZONTAL,
                                        resolution = 0.01,
                                        length=250)
                scale.grid(row=index+1, column=2, columnspan=3)
                trigVals.append( scale )

        initialize_UI()
        update_UI()


####
# FOR TESTING PURPOSES only
####

if __name__ == '__main__':
    root = tk.Tk()
    DataHandler(root).pack(side="top", fill="both",expand=True)
    root.mainloop()
