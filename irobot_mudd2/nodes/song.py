#!/usr/bin/env python
import roslib; roslib.load_manifest('irobot_mudd')
from irobot_mudd.srv import *
import rospy
import random

def sing(notes,durations):
    print notes
    print durations
    rospy.wait_for_service('song')
    song = rospy.ServiceProxy('song',Song)
    return song(notes,durations)

if __name__ == "__main__":
    notes = [36,48,55,60,64,67,70,72]
    notes += [46,58,65,70,74,77,80,82]
    notes += [56,68,75,80,84,87,90,92]
    durations = [32,16,16,8,8,8,4,4]*3
    #durations = [4] * 24
    sing(notes*4,durations*4)

    #nx = []
    #nd = []
    #for x in range(300):
    #    nx += [random.randint(31,127)]
    #    nd += [4]

    #sing(nx,nd)

