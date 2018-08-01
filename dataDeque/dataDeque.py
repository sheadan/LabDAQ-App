"""
dataDeque handles data from arduino. Data from arduino is expected in the format:
7 lines:
lines 1-6 are analog inputs A0-A5
line 7 is a timestamp in ms
"""

# Python 2 and Python 3
from collections import deque
import itertools
from time import time


class dataDeque:

    def __init__(self, recordFilename="", recordFlag=False, DequeLength=100):
        """Initialize data handling deque and recording params"""
        #Initialize data Deque with length as defined by initialization with data type of float
        self.dataDeque = deque( [[0.0]*6]*DequeLength, DequeLength )
        self.timeDeque = deque( [0.0]*DequeLength, DequeLength )
        self.dequeLength = DequeLength

        #initialize parameters for save file and flag
        self.recordFile = None
        self.recordFilename = recordFilename
        self.recordFlag = recordFlag


    def set_recording_file_name(self, dataSaveFilename):
        """Sets the filename for recorded data"""
        self.recordFilename = dataSaveFilename


    def set_recording_flag(self, flagValue):
        """Set the data recording flag. Note the functionality:
        Setting flag to true -> test file can be opened
         which decides whether or not data is recording to file"""
         # if setting the flag to true...
        if flagValue:
            try:
                self.recordFile = open( self.recordFilename, 'a' ) #test the file can be opened;
                self.recordFlag = flagValue #if successful, change flag value
                return True #and return True for GUI
            except IOError as err:
                print("Failed to open file") #if file opening fails, report failure
                self.recordFile = None # set the recordFile to none
                return False # and return False for GUI (indicating failure)
        # if setting the flag to false...
        else:
            if self.recordFile: #try closing any existing file
                self.recordFile.close()
            #set the recording flag
            self.recordFlag = flagValue
            #and return True for GUI
            return True


    def set_deque_length(self, newLength):
        #Create new data and time deques with newly specified length using
        # data from previous deque
        print( newLength )
        self.dequeLength = newLength
        self.dataDeque = deque( [[0.0]*6]*self.dequeLength, self.dequeLength)
        self.timeDeque = deque( [0.0]*self.dequeLength, self.dequeLength)


    def append_data(self, dataRow):
        """Handle data received from Arduino"""

        timePoint = dataRow.pop() #last value in data row is the timestamp
        dataRow = self.dataProcessor(dataRow) #process the values from the analog input

        # write values to file if recording
        # Note that due to positioning of this step, the data is pre-processed by processor before saving
        if self.recordFlag:
            self.writeData(timePoint, dataRow)

        # add the value to the dataDeque
        self.dataDeque.append(dataRow)
        self.timeDeque.append(timePoint)


    def dataProcessor(self, dataList):
        """Can be customized. Currently, this is configured for 5V reference voltage to convert input bits to voltage"""
        return [float(x)*(5./1024.) for x in dataList]


    def writeData(self, timePoint, dataRow):
        """Writes a data row to the file"""
        dataLine = ",".join(map(str, dataRow))
        line = "%s,%s" % (timePoint, dataLine)
        try:
            self.recordFile.write(line)
            self.recordFile.write('\n')
            #print "wrote data"
        except Exception as inst:
            #print "failed to write data"
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
