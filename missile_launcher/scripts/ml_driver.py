#!/usr/bin/env python
import roslib; roslib.load_manifest('missile_launcher')
import rospy

from missile_launcher.srv import *
from thunder_launcher import Launcher

import cmd, signal, time


class LauncherDriver:

   def __init__(self):
      """ initializes LauncherDriver object to have a Launcher
      """
      self.launcher = Launcher()
      
   ###########################################
   ## Responses to requests
   ## Note: each function takes in a required request variable req
   ##       that currently has no value due to *.srv files in
   ##       missile_launcher/srv/, but the driver is currently set
   ##       to have no service arguments. To change these responses
   ##       to have some input argument, you must first change the
   ##       .srv files and then remake the package with catkin_make.
   ###########################################
   def pan_left(self, req):
       """ Response to request to pan left """
       self.launcher.pan_left()
       return PanLeftResponse(True)

   def pan_right(self, req):
       """ Response to request to pan right """
       self.launcher.pan_right()
       return PanRightResponse(True)

   def tilt_up(self, req):
      """ Response to request to tilt up """
      self.launcher.tilt_up()
      return TiltUpResponse(True)

   def tilt_down(self, req):
      """ Response to request to tilt down """
      self.launcher.tilt_down()
      return TiltDownResponse(True)

   def stop(self, req):
      """ Response to request to stop """
      self.launcher.stop()
      return StopResponse(True)

   def fire(self, req):
      """ Response to request to fire missile """
      self.launcher.fire()
      return FireResponse(True)

# allows for command prompt interaction with launcher while driver is running
class prompt(cmd.Cmd):
   def __init__(self,robot):
      cmd.Cmd.__init__(self)
      self.prompt = '>>: '
      self.robot = robot.launcher
      self.robotWrap = robot
      self.intro = "\nReady!\nEnter help for commands"

   def do_quit(self,line):
      """ Attempts to stop and quit the program """
      self.quit()

      
   def do_panL(self,line):
      """ Executes pan_left, turning the launcher to the left """
      self.robot.pan_left()

   def do_panR(self,line):
      """ Executes pan_right, turning the launcher to the right """
      self.robot.pan_right()

   def do_tiltUp(self,line):
      """ Executes tilt_up, tilting the launcher up """
      self.robot.tilt_up()

   def do_tiltDown(self,line):
      """ Executes tilt_down, tilting the launcher down """
      self.robot.tilt_down()
      
   def do_stop(self,line):
      """ Executes stop, which stops the launcher's current action """
      self.robot.stop()

   def do_fire(self,line):
      """ Fires a missile! """
      self.robot.fire()
      
   def quit(self,*args):
     print "\nTrying to quit, if all else fails try ctrl-\\"
     rospy.core.signal_shutdown('keyboard interrupt')
     self.robot.stop()
     sys.exit(0)

def init_driver():
   """ initializes the driver and connects to ROS """
   global prompt
   
   print "Connecting to robot..."
   driver = LauncherDriver()

   print "Connecting to ROS..."
   rospy.init_node('missile_launcher')
   rospy.Service('panL', PanLeft, driver.pan_left)
   rospy.Service('panR', PanRight, driver.pan_right)
   rospy.Service('tiltUp', TiltUp, driver.tilt_up)
   rospy.Service('tiltDown', TiltDown, driver.tilt_down)
   rospy.Service('stop', Stop, driver.stop)
   rospy.Service('fire', Fire, driver.fire)


   prompt_object = prompt(driver)
   signal.signal(signal.SIGINT,prompt_object.quit)
   
   print "Ready to receive requests!"
   time.sleep(1)
   prompt_object.cmdloop()

   # only needed if prompt is removed
   #rospy.spin()

if __name__ == "__main__":
    init_driver()
