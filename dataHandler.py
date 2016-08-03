"""
The data handler is a TkInter gui for:
- toggle data saving on/off
- select file name/location
"""

from dataDeque.dataDeque import dataDeque as dD

import os
DEFAULTSAVELOCATION = "".join( [
                        os.path.dirname(os.path.realpath(__file__)),
                        "\data\\test.txt"
                        ])
# Python 3
# import tkinter as tk
# from tkinter import ttk
# from tkinter import filedialog

# Python 2
import Tkinter as tk
import ttk
import tkFileDialog as filedialog


class DataHandler(tk.Frame):

    def __init__(self, parent=None, dataDeque=None, *args, **kwargs):
        #Initialize TkInter frame and define parent
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # initialize  data deque
        if not dataDeque:
            self.dataDeque = dD()
        else:
            self.dataDeque = dataDeque

        #generate UI elements
        self.create_filename_selector()
        self.create_recording_checkbox()


    def create_filename_selector(self):
        """create filename selector to choose where to save data"""
        # label for the filename location tk variable
        self.filename = tk.StringVar()
        self.update_record_file_name(DEFAULTSAVELOCATION)
        # place labels into UI
        tk.Label(self, text='Save to:').grid(row=1, column=0, sticky='e')
        tk.Label(self, textvariable=self.filename).grid(row=1, column=1, columnspan=2)
        # button for choosing file name, placed into UI
        tk.Button(self, text='Select...', command=self.ask_filename).grid(row=1, column=3)


    def create_recording_checkbox(self):
        """UI checkbox and label for recording data to file"""
        # create Tk boolean variable
        self.recordBool=tk.BooleanVar()
        self.recordBool.set(0)
        #Check button, and packing
        tk.Checkbutton(self, text="Record data to file?",
                variable=self.recordBool, command=self.update_record_flag,
                onvalue=1, offvalue=0).grid(row=2, column=0, columnspan=3)


    def ask_filename(self):
        """File dialog for choosing file save location"""
        # settings for file dialog
        options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['initialdir'] = os.path.dirname(os.path.realpath(__file__))
        options['initialfile'] = 'myfile.txt'
        options['parent'] = self.parent
        options['title'] = 'This is a title'
        # get filename
        fn = filedialog.asksaveasfilename(**options)
        self.update_record_file_name( fn )

    def update_record_flag(self):
        """Update current value of recording flag"""
        #get current value of the recording Boolean
        curVal= self.recordBool.get()
        # attempt to change the flag. the function in dataDeque returns a Boolean
        # which indicates cuccess/failure in changing flag
        if self.dataDeque.set_recording_flag( curVal ):
            return
        else:
            opposite = not curVal
            self.recordBool.set(opposite)

    def update_record_file_name(self, fn):
        """Update the save file name/location"""
        self.dataDeque.set_recording_file_name( fn )
        self.filename.set(fn)


####
# FOR TESTING PURPOSES only
####

if __name__ == '__main__':
    root = tk.Tk()
    DataHandler(root).pack(side="top", fill="both",expand=True)
    root.mainloop()
