"""
Channel class models
"""
from alarm import Alarm
from collections import deque
import itertools


class Channel:

    def __init__(self, dequeLength=100):
        """Initialize channel info"""
        #initialize voltage and time data arrays
        self.data = deque( [0.0]*dequeLength, dequeLength )
        self.time = deque( [0.0]*dequeLength, dequeLength )
        # intialize alarm to None; assign when set
        self.alarm = None
        # prepare variable for buffer size
        self.dequeLength = dequeLength


    def set_alarm(self, valueToTrack):
        self.alarm = Alarm( valueToTrack )

    def check_alarms(self, valueToCheck):
        """checks each alarm in alarms array"""
        if self.alarm:
            return self.alarm.check_alarm( valueToCheck )
        else:
            return False

    def remove_alarm(self):
        self.alarm = None

    def append_data(self, dataPoint, timePoint):
        """Handle data received from Arduino"""
        # add the data-processed value to the dataDeque
        self.data.append(dataPoint)
        self.time.append(timePoint)
        # return alarm status
        # check data to add against alarms
        return self.check_alarms( dataPoint )


    def set_deque_length(self, newLength):
        #Create new data and time deques with newly specified length using
        # data from previous deque
        self.dequeLength = newLength
        self.data = deque( self.data, self.dequeLength )
        self.time = deque( self.time, self.dequeLength )
