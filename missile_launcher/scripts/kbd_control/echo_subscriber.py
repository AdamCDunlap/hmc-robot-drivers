#!/usr/bin/env python
import roslib; roslib.load_manifest('missile_launcher')
import rospy
from std_msgs.msg import String
from missile_launcher.srv import *

import time
import math

####
# echo_subscriber.py ~ showing off ROS subscribing...
####

class Data: pass
D=Data()


def main():
    """ establishes our ROS node
        subscribes to the published stream (at stream_name)
    """
    global D
    init()
    
    rospy.init_node('listener', anonymous=True)  # usual node-naming

    # the key piece of information is the name of the published stream
    stream_name = 'text_data'

    # this subscribes to the stream
    # (1) it names the stream (stream_name)
    # (2) it indicates the type of message received (String)
    # (3) it indicates a function (callback) to be called w/ each message
    rospy.Subscriber( stream_name, String, callback )

    # wait until rospy.signal_shutdown
    rospy.spin()  



####
# callback ~ called with each published message
####
def callback(data):
    """ This function is called for each published message
    """
    message = data.data
    print "I received the string", message

    if message == "a" or message =="A":
        D.panL()
    elif message == "d" or message =="D":
        D.panR()
    elif message == "w" or message =="W":
        D.tiltUp()
    elif message == "s" or message =="S":
        D.tiltDown()
    elif message == "e" or message =="E":
        D.stop()
    elif message == " ":
        D.fire()
        
    time.sleep(0.05)
    # if the message is the string 'q', we shutdown
    if message == 'q':
        D.stop()
        rospy.signal_shutdown("Quit requested.")
        

def init():
    """ returns an object (tank) that allows you
       to set the velocities of the robot's wheels
    """
    global D # to hold system state

    # obtaining service proxies to allow keyboard control
    rospy.wait_for_service('panL')
    rospy.wait_for_service('panR')
    rospy.wait_for_service('tiltUp')
    rospy.wait_for_service('tiltDown')
    rospy.wait_for_service('fire')
    rospy.wait_for_service('stop')
    D.panL     = rospy.ServiceProxy('panL', PanLeft)
    D.panR     = rospy.ServiceProxy('panR', PanRight)
    D.tiltUp   = rospy.ServiceProxy('tiltUp', TiltUp)
    D.tiltDown = rospy.ServiceProxy('tiltDown', TiltDown)
    D.fire     = rospy.ServiceProxy('fire', Fire)
    D.stop     = rospy.ServiceProxy('stop', Stop)
    
####
# It all starts here...
#
# This is the "main" trick: it tells Python what code to run
# when you execute this file as a stand-alone script:
####

if __name__ == '__main__':
    main()
