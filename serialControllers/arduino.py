""" Class that handles acquiring the serial data
    from the arduino for Data Acquisiton
    NOTE: baud rate is set from serial device handler serialSelector.py
"""

import serial
import time

class Arduino(object):
    def __init__(self):
        self.ser = None

    def connect_to_arduino(self, usbport, baud=115200):
        self.ser = None
        self.ser = serial.Serial(
             port=usbport,
             baudrate=baud,
             bytesize=serial.EIGHTBITS,
             parity=serial.PARITY_NONE,
             stopbits=serial.STOPBITS_ONE,
             timeout=1,
             xonxoff=0,
             rtscts=0,
             interCharTimeout=None
            )


    def poll(self):
        """Retrieve data from arduino in format:
        Line 1: Analog 0 reading
        Line 2: Analog 1 reading
        Line 3: Analog 2 reading
        Line 4: Analog 3 reading
        Line 5: Analog 4 reading
        Line 6: Analog 5 reading
        Line 7: Timestamp in milliseconds
        """
        self.ser.flush() # flush before sending signal
        self.ser.write('w') # send signal telling Arduino to send data

        # now read lines sent by the Arduino and store into list
        data = []

        # reading the analog channels; seems to fail first few times so added an exception
        try:
            # read the 6 analog channels and the timestamp
            for i in range(0,7):
                line = self.ser.readline() #read the line
                val = int(line[0:-2]) #strips newline char and converts value to int
                data.append( val ) # append to data array

            dataFlag = True # set data-read flag as true to return value

        except:
            #print "no data this round"
            dataFlag = False #in case data reading fails, no data will be sent to data handler

        return [data, dataFlag]


    def trigger_alarm(self):
        """ Trigger alarm function programmed into Arduino firmware """
        self.ser.flush() # flush before sending signal
        self.ser.write('a') #send signal telling Arduino to sound the alarm


    def disconnect(self):
        """disconnect from arduino device"""
        if self.is_connected():
            self.ser.close()
            self.ser = None


    def is_connected(self):
        """returns connection status (true=connected, false=disconnected)"""
        if self.ser:
            return self.ser.isOpen()
        else:
            return False
