#!/usr/bin/env python

# You will need these next two lines so that the service
# communication works
import roslib; roslib.load_manifest('irobot_mudd')
from irobot_mudd.srv import *
import rospy

if __name__ == "__main__":
    # Do not proceed until the song service is available
    rospy.wait_for_service('song')
    # create a connection to the song service
    # now song(a,b) calls are equivalent to rosservice call song a b
    song = rospy.ServiceProxy('song',Song)

    # Notes of an overtone series
    # 60 cooresponds to middle c.  Check the create documentation for
    # more information about the notes
    notes = [36,48,55,60,64,67,70,72]
    # Cooresponding note durations in 64ths of seconds.  4 is the smallest
    # that will play
    durations = [32,16,16,8,8,8,4,4]
    # Finally send the notes and durations to the service to play
    song(notes,durations)

