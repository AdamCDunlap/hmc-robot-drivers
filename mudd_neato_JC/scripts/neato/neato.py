#!/usr/bin/env python

##############################
## Driver for the "good robot"
##############################

# Generic driver for the Neato XV-11 Robot Vacuum
# Copyright (c) 2010 University at Albany. All right reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the University at Albany nor the names of its 
#       contributors may be used to endorse or promote products derived 
#       from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL VANADIUM LABS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#################################################################################
###
### THIS FILE UPDATED MAY&JUNE 2013 AT HARVEY MUDD COLLEGE
###
#################################################################################




"""
neato_driver.py is a generic driver for the Neato XV-11 Robotic Vacuum.
ROS Bindings can be found in the neato_node package.
"""

import serial
import time
from struct import pack
from struct import unpack
from threading import Thread

from datetime import datetime

BASE_WIDTH = 248    # millimeters
MAX_SPEED = 300    # millimeters/second
MAX_DISTANCE = 10000 # millimeters
MAX_DISTANCE_NEG = -10000 # millimeters
STOP_DISTANCE = 1 # millimeters
DEFAULTREQ = 2 # digital sensor and button requests
REQTIME = 0.10 # default time for a single request

lines = ""
line_split = []




class Monitor(Thread):
    """Monitor thread for getting the sensor data"""
    def __init__(self, watchdog, state, range_data, xv11, requestSensors, readSensors, sendAll, update):
        Thread.__init__(self)
        self.watchdog = watchdog
        self.state = state
        self.range_data = range_data
        self.xv11 = xv11
        self.update = update
        self.requestSensors = requestSensors
        self.readSensors = readSensors
        self.sendAll = sendAll

    def run(self):

        
        while (len(self.watchdog) == 0):

            # send all queued commands
            self.sendAll()

            # request all current sensor and laser data
            self.requestSensors()
            self.sendAll()
            time.sleep(.05)

            # receive and handle sensor and laser data
            self.readSensors()

            # update the sensor and laser data    
            self.update()

class xv11():
    """Wrapper class for the xv11 neato robot"""

    def __init__(self, port="/dev/ttyUSB0"):
        """constructor for the Create"""

        # Find the right USB port to connect
        for i in range(10):
            try:
                port = "/dev/ttyUSB" + str(i)
                self.port = serial.Serial(port,115200,timeout=0.01)
                print "The port number is /dev/ttyUSB" + str(i)
                break
            except:
                try:
                    port = "/dev/ttyACM" + str(i)
                    self.port = serial.Serial(port,115200,timeout=0.01)
                    print "The port number is /dev/ttyACM" + str(i)
                    break
                except:
                    pass

        # Storage for motor and sensor information
        self.state = {"LeftWheel_PositionInMM": 0, "RightWheel_PositionInMM": 0}
        self.update = lambda : ''
        self.runRef = []
        self.range_data = [0]*360
        self.queue = []
        
        # Default number is 2 as only digital sensor and button data are needed
        self.reqtime = REQTIME
        self.reqnum = DEFAULTREQ
        print "Finish the initialization"

    def start(self):
        # turn things on
        self.send("testmode on\n")
        time.sleep(2)
        self.send("setldsrotation on\n")
        time.sleep(2)
        self.port.flushInput()
        
        print "Set test mode on, start to get the data."

        monitor = Monitor(self.runRef, self.state, self.range_data, self, self.requestSensors, self.readSensors, self.__sendAll, self.update)
        monitor.start()


    def send(self, string):
        
        def lmbda():
            self.__sendNow(string)
            
        self.queue.append(lmbda)



    def __sendNow(self, data):        
        self.port.write(data)


    def __sendAll(self):

        for send in self.queue:
            send()
        self.queue = []

        
    def exit(self):
        self.setLDS("off")
        self.setTestMode("off")
        self.__sendAll()
        time.sleep(1)
        self.runRef.append('exit')
        self.port.flushInput()
        time.sleep(1.0)
        self.port.flushInput()
        time.sleep(1.0)
        self.port.flushInput()

    def setTestMode(self, value):
        """ Turn test mode on/off. """
        self.send("testmode " + value + "\n")

    def setLDS(self, value):
        self.send("setldsrotation " + value + "\n")

   

    
    #######################################
    ## Set Motors
    #######################################

    def tank(self,l,r):
        """ Set motors to run, but the absolute value of left and right speed should be the same"""
	if l == 0 and r == 0:
	    r_distance = STOP_DISTANCE
            l_distance = STOP_DISTANCE
        elif abs(l) > abs(r):
            proportion = 1.0* abs(r) / abs(l)
            l_distance = MAX_DISTANCE
            r_distance = int(proportion * MAX_DISTANCE)
            if r_distance == 0:
                r_distance = STOP_DISTANCE
        else:
            proportion = 1.0* abs(l) / abs(r)
            l_distance = int(proportion * MAX_DISTANCE)
            r_distance = MAX_DISTANCE
            if l_distance == 0:
                l_distance = STOP_DISTANCE
                    
        speed = max(abs(l),abs(r))
        if speed > MAX_SPEED:
            print str(speed) + " is larger than the maximum value, set it to be 300"
            speed = MAX_SPEED
    
        if l > 0 and r < 0:    
            self.send("setmotor "+str(l_distance)+" "+str(-r_distance)+" "+str(int(speed))+"\n")
        elif l < 0 and r > 0:
            self.send("setmotor "+str(-l_distance)+" "+str(r_distance)+" "+str(int(speed))+"\n")
        elif l > 0 and r > 0:
            self.send("setmotor "+str(l_distance)+" "+str(r_distance)+" "+str(int(speed))+"\n")
        elif l < 0 and r < 0:
            self.send("setmotor "+str(-l_distance)+" "+str(-r_distance)+" "+str(int(speed))+"\n")
        else:
            self.send("setmotor "+str(l_distance)+" "+str(r_distance)+" "+str(int(MAX_SPEED))+"\n")


    def stop(self):
        self.send("setmotor "+str(STOP_DISTANCE)+" "+str(STOP_DISTANCE)+" "+str(int(MAX_SPEED))+"\n")

    #####################################

    def requestSensors(self):
        """ send request for digital sensor and button data into queue """
        self.send("getdigitalsensors\n")
        self.send("getbuttons\n")
        self.send("getldsscan\n")


        
    def readSensors(self):
        """ parses all sensor data and updates the dictionary """
        global lines
        global line_split
        
        line = ""
        num = self.port.inWaiting()

        while num > 0:
            line = self.port.readline()
            lines += line
            num = self.port.inWaiting()
##  "bad robot" has those lines
##            if num < 100:
##                time.sleep(0.015)
##        print lines
        line_split = lines.split('\x1a')
        line_split = [x.split('\r\n') for x in line_split]

        self.receiveData()

        lines = ""
        line_split = []

    def receiveData(self):
        global lines
        global line_split

        for package in line_split:
            if package[0] == 'getldsscan':
                for vals in package:                
                    try:
                        vals = vals.split(",")
                        a = int(vals[0])
                        r = int(vals[1])
                        self.range_data[a] = (r/1000.0)
                    except:
                        pass
            else:
                for pair in package:
                    try:
                        values = pair.split(',')
                        self.state[values[0]] = int(values[1])
                    except:
                        pass
        


    def getAnalogSensors(self):
        """ get the analog sensor data """
        self.reqnum += 1
        self.send("getanalogsensors\n")

    def getMotors(self):
        """ get the motor sensor data """
        self.reqnum += 1
        self.send("getmotors\n")

    def getCharger(self):
        """ get the charger sensor data """
        self.reqnum += 1
        self.send("getcharger\n")


    def setBacklight(self, value):
        if value > 0:
            self.send("setled backlighton") 
        else:
            self.send("setled backlightoff")

    def getErr(self):
        self.send("geterr clear\n")

    def playSound(self,num):
        """Play the sound"""
        self.send("playsound " + str(int(num)) + "\n")

    def shutdown(self):
        """Shut down the robot"""
        self.send("setsystemmode shutdown\n")

    def hibernate(self):
        """Start hibernate operation"""
        self.send("setsystemmode hibernate\n")

    def standby(self):
        """Start standby operation"""
        self.send("setsystemmode standby\n")

    def backLightOn(self):
        """LCD Backlight On"""
        self.send("setLED backlighton\n")

    def backLightOff(self):
        """LCD Backlight Off"""
        self.send("setLED backlightoff\n")

    def buttonAmber(self):
        """Start Button Amber"""
        self.send("setLED buttonamber\n")

    def buttonGreen(self):
        """Start Button Green"""
        self.send("setLED buttongreen\n")

    def LEDRed(self):
        """Start Red LED"""
        self.send("setLED LEDRed\n")

    def LEDGreen(self):
        """Start Green LED"""
        self.send("setLED LEDGreen\n")

    def buttonAmberDim(self):
        """Start Button Amber Dim"""
        self.send("setLED buttonamberdim\n")

    def buttonGreenDim(self):
        """Start Button Green Dim"""
        self.send("setLED buttongreendim\n")

    def buttonOff(self):
        """Start Button off"""
        self.send("setLED buttonoff\n")
