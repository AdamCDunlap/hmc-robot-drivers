#!/usr/bin/env python

# You will need these next two lines so that the service
# communication works
import roslib; roslib.load_manifest('irobot_mudd')
from irobot_mudd.srv import *
import rospy

if __name__ == "__main__":
    # Do not proceed until the tank service is available
    rospy.wait_for_service('tank')
    # create a connection to the song service
    # now tank(a,b) calls are equivalent to rosservice call tank a b
    tank = rospy.ServiceProxy('tank',Tank)

    # Set the motor speed to 100
    tank(100,100) 
    # Move for 4.2 seconds
    rospy.sleep(4.2)
    # Turn for 1 second
    tank(-100,100)
    rospy.sleep(1)
    # Move backwards for 3 seconds
    tank(-42,-42)
    rospy.sleep(3)

    # Make sure you stop the robot at the end of your program or it will continue on happily
    # In case of run away robots you can always manual send a stop signal to the service from 
    # the terminal
    # >>> rosservice call tank 0 0
    tank(0,0)
