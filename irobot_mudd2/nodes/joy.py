#!/usr/bin/env python

import roslib; roslib.load_manifest('irobot_mudd')
from irobot_mudd.srv import *
from irobot_mudd.msg import *
from std_msgs import msg
import rospy
import pygame

print "waiting"
rospy.wait_for_service("/tank")
tank = rospy.ServiceProxy("/tank", Tank)
servoP = rospy.Publisher("/pan_controller/command", msg.Float64)
rospy.init_node("joy_controller")
print "connected"

pygame.init()
j = pygame.joystick.Joystick(0)
j.init()

while True:
    pygame.event.pump()
    x = -j.get_axis(1)
    theta = j.get_axis(0)

    if abs(x) < .17:
      x = 0
    if abs(theta) < .17:
      theta = 0

    speedl = (x * 300) + (theta * 250)
    speedr = (x * 300) - (theta * 250)
    tank(speedl,speedr)
    
    if j.get_button(3):
      servoP.publish(0)
    elif j.get_button(0):
      servoP.publish(1)
    elif j.get_button(4):
      servoP.publish(2)

    elif j.get_button(2):
      servoP.publish(-1)
    elif j.get_button(5):
      servoP.publish(-2)

    rospy.sleep(.05)


