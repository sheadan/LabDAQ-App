'''
Define a function that gets the names of all available serial ports
'''

import sys
import glob
import serial


def getSerialPorts():
    ports = []
    if sys.platform.startswith('win'):
        for i in range(256):
            a = "COM%s" % i
            ports.append( a )
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported Platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial( port )
            s.close()
            result.append(port)
        except Exception as inst:
            #print(type(inst))    # the exception instance
            #print(inst.args)     # arguments stored in .args
            pass

    return result
