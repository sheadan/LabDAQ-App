"""
dataDeque handles data from arduino. Data from arduino is expected in the format:
7 lines:
lines 1-6 are analog inputs A0-A5
line 7 is a timestamp in ms
"""
#import local dependencies
from alarm import Alarm
from channel import Channel
from datasaver import DataSaver

# Python 2 and Python 3
from collections import deque
import itertools


class DataHandler( DataSaver ):

    def __init__(self, numChannels=6, dequeLength=100):
        """Initialize data handling deque and recording params"""
        # run initialization for DataSaver
        DataSaver.__init__(self)
        # attribute for how many points are to be collected
        self.bufferSize = dequeLength
        #Initialize channel object for number of channels to track
        self.channels=[]
        for channel in range(numChannels):
            self.channels.append( Channel(dequeLength) )


    def append_data(self, dataRow):
        """Handle data received from Arduino"""
        #last value in data row is the timestamp
        timePoint = dataRow.pop()
        # process other voltage values
        dataRow = self.data_processor(dataRow)
        # write the data if the record flag is appropriately set
        self.write_data(dataRow, timePoint)

        # assert that the number of channels (length of channel array) is equal
        # to the number of data points
        # assert len(self.channels) == len(dataRow)

        #pick up signal notification by appending results to array
        alarmStatuses=alarmTriggered = False

        # append the data to the channels (channels check for alarms)
        for (index,dataPoint) in enumerate(dataRow):
            alarmStatus= self.channels[index].append_data(dataPoint,timePoint)
            if alarmStatus:
                alarmTriggered=True

        return alarmTriggered

    def update_channel_data_size(self, newDequeLength):
        for channel in self.channels:
            channel.set_deque_length(newDequeLength)

    def get_data(self):
        """return all the data! for plotting"""
        x = [channel.data for channel in self.channels]
        print x
        return x


    def data_processor(self, dataList):
        """Can be customized. Currently, this is configured for 5V reference voltage to convert input bits to voltage"""
        return [float(x)*(5./1024.) for x in dataList]
