# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import numpy as np
import Tkinter as tk
import ttk
import sys
import math


class PlotHandlerUI(tk.Frame):
    def __init__(self, parent, dataHandler, *args, **kwargs):
        """Initialize plotting frame, data deque, and number of plots"""
        # TkInter frame and define parent
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # initialize attribute for dataHandler
        self.dataHandler = dataHandler

        #initialize attributes for # of plots
        self.numPlots = len( dataHandler.channels )

        # create frame for MPL figure
        self.create_plot_panel()
        # create menu for number of plots
        self.create_plot_control_panel()


    def create_plot_panel(self):
        """Create matplotlib figure, subplots (via init_plots), and canvas"""
        # generate figure (assign dpi to image)
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.figure.subplots_adjust(hspace=.5) # adjust sub plot spacing
        # generate canvas
        self.plotCanvas = FigureCanvasTkAgg(self.figure, master=self)
        # show canvas
        self.plotCanvas.show()
        # pack into UI
        self.plotCanvas.get_tk_widget().grid(row=0, column=0, columnspan=6)
        self.plotCanvas._tkcanvas.grid(row=0, column=0, columnspan=6)


    def init_plots(self):
        """Generating a subplot for each plot to be added to figure"""
        # clear figure contents
        self.figure.clear()
        # create list for subplots
        self.axes = []
        # calculate number of rows and columns based on number of plots
        numRows = math.ceil(self.numPlots/2.)
        numColumns = math.ceil(self.numPlots/numRows)
        # populat subplot list
        for i in range(1,self.numPlots+1):
            self.axes.append(self.figure.add_subplot(numColumns,numRows,i, xticks=[], yticks=[]))


    def create_plot_control_panel(self):
        """Control panel for choosing number of plots to display"""
        # plot number control button
        scale = tk.Scale(master=self, from_=1, to=6,
                                command=self.update_num_plots,
                                orient=tk.HORIZONTAL,
                                length=250)
        scale.set( self.numPlots )
        scale.grid(row=1, column=1, columnspan=4)
        tk.Label(master=self, text="Number of plots:").grid(row=1,column=0)

    def update_num_plots(self, value):
        # reassign value of number of plots
        self.numPlots = int(value)
        #repeat plot initialization based new number of plots
        self.init_plots()
        self.plotCanvas.draw()

    def update_plots(self):
        """For live-updating of plots"""
        assert( self.numPlots <= len(self.dataHandler.channels) )
        for i in range(0,self.numPlots):
            channel = self.dataHandler.channels[i]
            data = list(channel.data)
            num_points = len(data)
            axes = self.axes[i]
            axes.plot(range(0,num_points), data,'k', color='c')
            axes.set_title('CH A'+str(i))
            axes.set_ylim(0,5)
            axes.set_yticks([0, 1, 2, 3, 4, 5])
            axes.set_xticks([])
            axes.hold(False)
            if channel.alarm:
                axes.axhline(y=channel.alarm.triggerValue, xmax=num_points, color='c')

        self.plotCanvas.draw()





####
# FOR TESTING PURPOSES only
####

if __name__ == '__main__':
    root = tk.Tk()
    PlotHandler(root).pack(side="top", fill="both",expand=True)
    root.mainloop()
