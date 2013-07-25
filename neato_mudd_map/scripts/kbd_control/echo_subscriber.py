#!/usr/bin/env python
import roslib; roslib.load_manifest('neato_mudd')
import rospy
import neato_mudd
from std_msgs.msg import String
from neato_mudd.srv import *
from neato_mudd.msg import *
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

    if message == "a" or message =="Q":
        D.tank(-100, 100)
    elif message == "d" or message =="S":
        D.tank(100, -100)
    elif message == "w" or message =="R":
        D.tank(220, 220)
    elif message == "s" or message =="T":
        D.tank(-220, -220)
    elif message == " ":
        D.stop()
    time.sleep(0.1)
    # if the message is the string 'q', we shutdown
    if message == 'q':
        D.tank(0,0)
        rospy.signal_shutdown("Quit requested.")
        

def init():
    """ returns an object (tank) that allows you
       to set the velocities of the robot's wheels
    """
    global D # to hold system state

    # we need to give our program a ROS node name
    # the name is not important, so we use "lab1_node"
    #rospy.init_node('lab1_node', anonymous=True)
    
    # we obtain the tank service
    rospy.wait_for_service('tank') # wait until the motors are available
    D.tank = rospy.ServiceProxy('tank', Tank) # D.tank is our "driver"

    # we obtain the stop service
    rospy.wait_for_service('stop') # wait until the stop service is available
    D.stop = rospy.ServiceProxy('stop', Stop)
    
####
# It all starts here...
#
# This is the "main" trick: it tells Python what code to run
# when you execute this file as a stand-alone script:
####

if __name__ == '__main__':
    main()
