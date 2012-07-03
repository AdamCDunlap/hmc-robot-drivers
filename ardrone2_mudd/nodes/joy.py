#!/usr/bin/env python

import roslib; roslib.load_manifest('ardrone2_mudd')
from ardrone2_mudd.srv import *
from ardrone2_mudd.msg import *
import rospy
import pygame

def navDataUpdate(data):
  global commands
  global lastsent
  global helistr
  global droneData

  droneData = data
  sys.stdout.write("\r\t [alt: %i] \t [phi: %i psi: %i theta: %i] \t [vx: %i vy: %i vz: %i] \t [bat: %i  state: %i]\n" \
      %
      (data.altitude,data.phi,data.psi,data.theta,data.vx,data.vy,data.vz,data.batLevel,data.ctrlState))
  sys.stdout.write("\rLast sent: %s\n" % (lastsent))
  sys.stdout.write("\033[A")
  sys.stdout.write("\033[A")
  sys.stdout.flush()

rospy.wait_for_service("ardrone2/heli")
heli = rospy.ServiceProxy("ardrone2/heli", Control)
rospy.Subscriber("ardrone2/navData",navData, navDataUpdate, queue_size=1)
print "connected"

pygame.init()
j = pygame.joystick.Joystick(0)
j.init()

while True:
    pygame.event.pump()

    flag = 0
    phi = j.get_axis(0)
    theta = j.get_axis(1)
    gaz = j.get_axis(3)
    yaw = j.get_axis(2)

    if j.get_button(3):
        heli(3,0,0,0,0)
    if j.get_button(1):
        heli(2,0,0,0,0)
    if j.get_button(0):
        heli(4,0,0,0,0)

    if abs(phi) < .17:
        phi = 0
    if abs(theta) < .17:
        theta = 0
    if abs(gaz) < .17:
        gaz = 0
    if abs(yaw) < .17:
        yaw = 0

    if ( abs(phi) > 0 or abs(theta) > 0):
        flag = 1
    #helistr = "heli %i %.3f %.3f %.3f %.3f" % (flag,phi,theta,-gaz,yaw)
    heli(flag,phi,theta,-gaz,yaw)
    #rospy.sleep(.01)


