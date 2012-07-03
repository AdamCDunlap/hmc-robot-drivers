#!/usr/bin/env python

import roslib; roslib.load_manifest('irobot_mudd')
from irobot_mudd.srv import *
from irobot_mudd.msg import *
import rospy
import pygame

rospy.wait_for_service("tank")
tank = rospy.ServiceProxy("tank", Tank)
print "connected"

pygame.init()
j = pygame.joystick.Joystick(0)
j.init()

while True:
    pygame.event.pump()

    flag = 0
    x = -j.get_axis(1)
    theta = j.get_axis(0)

    if abs(x) < .17:
      x = 0
    if abs(theta) < .17:
      theta = 0

    speedl = (x * 300) + (theta * 250)
    speedr = (x * 300) - (theta * 250)
    tank(speedl,speedr)
    rospy.sleep(.05)


