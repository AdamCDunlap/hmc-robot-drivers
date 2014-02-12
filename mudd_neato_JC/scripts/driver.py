#!/usr/bin/python
import roslib; roslib.load_manifest('neato_mudd')
import rospy
from neato_mudd.srv import *
from neato_mudd.msg import *
from time import sleep
from neato import xv11
from datetime import datetime
from math import sin, cos, pi
from neato import xv11

from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.broadcaster import TransformBroadcaster

import cmd,sys,signal,serial,os

########################################################
# ROS wrapper for the Neato XV11 robot. Designed for
# use at Harvey Mudd College for Prof. Zachary Dodds'
# robotics lab.
# Author: Zakkai Davidson
# Date: 6/5/13
# ROS Version: Groovy
########################################################
# NOTE: Current setup for the sensor broadcaster is
#       to publish a subset of sensor data. To change
#       topic to include all sensor data, change the
#       publisher class to be NeatoSensors_All and
#       the class of sensorData in NeatoDriver.sense()
#       to also be NeatoSensors_All
########################################################

class NeatoDriver:
    def __init__(self):
        self.neato = xv11()
        self.sensorPub = rospy.Publisher('neatoSensors', NeatoSensors) # see NOTE above
        self.rangePub  = rospy.Publisher('laserRangeData',LaserRangeData)
        self.fields = self.neato.state.keys() # gets all of the sensors fields from the Neato
        self.neato.update = self.sense
        
    def start(self):
        self.neato.start()
        
    def stop(self, req):
        self.neato.stop()
        return StopResponse(True)

    def tank(self, req):
        self.neato.tank(req.left,req.right)
        return TankResponse(True)

    def playSound(self, req):
        """ plays a sound from the Neato's database.
            num goes from 0 to 20 inclusive
        """
        self.neato.playSound(req.num)
        return PlaySoundResponse(True)

    def sense(self):
        """ collects sensor data from the Neato and publishes
            it to the neatoSensors topic
        """
        # receive and publish sensor data
        self.fields = self.neato.state.keys() # update sensor fields
        sensor_data  = NeatoSensors() # see NOTE above
        for field in self.fields:
            try:
                sensor_data.__setattr__(field, self.neato.state[field])
            except:
                pass
        self.sensorPub.publish(sensor_data)

        # receive and publish laser range data
        range_data = LaserRangeData()
        range_data.__setattr__("range_data", self.neato.range_data)
        self.rangePub.publish(range_data)

class prompt(cmd.Cmd):
    def __init__(self,robot):
        cmd.Cmd.__init__(self)
        self.prompt = '>>: '
        self.robot = robot.neato
        self.robotWrap = robot
        self.intro = "\nReady!\nEnter help for commands"

    def do_quit(self,line):
        """ Attempts to stop and quit the program """
        self.robot.exit()
        self.quit()

    def do_stop(self,line):
        """ Executes stop """
        print "Trying to stop the robot"
        self.robot.stop()

    def do_tank(self,line):
        """ Executes tank LEFT RIGHT """
        lineS = line.split()
        try:
            left = int(lineS[0])
            right = int(lineS[1])
            self.robot.tank(left,right)
        except:
            print "Invalid arguments " + line

    def do_playSound(self, line):
        """ Plays sound 0 - 20 """
        lineS = line.split()
        try:
            sound = int(lineS[0])
            self.robot.playSound(sound)
        except:
            print "Invalid arguments " + line


    def quit(self,*args):
        print "\nTrying to quit gracefully, if all else fails try ctrl-\\"
        rospy.core.signal_shutdown('keyboard interrupt')
        self.robot.exit()
        sys.exit(0)

if __name__ == '__main__':
    node = rospy.init_node('neato_mudd')
    
    print "Connecting to robot"
    driver = NeatoDriver()
    
    print "Connecting to ROS"
    rospy.Service('tank',Tank,driver.tank)
    rospy.Service('stop',Stop,driver.stop)
    rospy.Service('playSound',PlaySound,driver.playSound)

    prompt = prompt(driver)
    signal.signal(signal.SIGINT,prompt.quit)

    print "Starting robot control"
    sleep(1)
    driver.start()
    sleep(1)

    try:
        prompt.cmdloop()
    except serial.SerialException:
        print "\n Lost connection to robot! \n"
        prompt.quit()
        

