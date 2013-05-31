#!/usr/bin/env python
import roslib; roslib.load_manifest('missile_launcher')

import sys

import rospy
from missile_launcher.srv import *

def ml_client():
    rospy.wait_for_service('fire')
    try:
        fire = rospy.ServiceProxy('fire', Fire)
        resp1 = fire()
        print "Duck and cover!"
        return resp1
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def usage():
    return "Try again with no arguments"

if __name__ == "__main__":
    if len(sys.argv) != 1:
        print usage()
        sys.exit(1)
    ml_client()
