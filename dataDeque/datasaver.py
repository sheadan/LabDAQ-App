"""
DataSaver handles saving data to file
"""

# Python 2 and Python 3
import itertools
import os
CURRENT_PATH = "".join( [os.getcwd(), "\data\\test.txt"] )


class DataSaver:

    def __init__( self, recordFilename=CURRENT_PATH, recordFlag=False ):
        """Initialize data handling deque and recording params"""
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
                self.recordFlag = True #if successful, change flag value
                return True #and return True for GUI
            except IOError as err:
                print "Failed to open file" #if file opening fails, report failure
                self.recordFile = None # set the recordFile to none
                self.recordFlag = False
                return False # and return False for GUI (indicating failure)
        # if setting the flag to false, close existing file first, and return true
        else:
            if self.recordFile: self.recordFile.close()
            self.recordFlag = flagValue
            return True


    def write_data(self, dataRow, timePoint):
        """Writes a data row to the file"""
        #only proceed if record flag is set
        if self.recordFlag:
            # format timepoint as a String
            timePoint = repr(timePoint)
            # format timept to write to file
            timePoint += ","
            #prep data row array for writing
            dataRow = ",".join(map(str, dataRow))
            dataRow += '\n'
            #try writing to file, print if there is an error
            try:
                self.recordFile.write(timePoint)
                self.recordFile.write(dataRow)

            except Exception as inst:
                print(type(inst))    # the exception instance
                print(inst.args)     # arguments stored in .args
