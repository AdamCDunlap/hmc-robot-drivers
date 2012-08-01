#!/usr/bin/env python
import roslib; roslib.load_manifest("ardrone2_mudd_gazebo")
import rospy
from gazebo.srv import GetModelState, SetModelState
from ardrone2_mudd.srv import Control
from geometry_msgs.msg import Twist,Pose
from math import cos,sin
import random
import tf

getState = 0
setState = 0
flag = 0
roll = 0
pitch = 0
gaz = 0
yaw = 0
droneName = "ardrone"
turbMult = 3

controlMult = 2

def main():
  global getState
  global setState
  global flag
  global roll
  global pitch
  global gaz
  global yaw
  global airborne
  airborne = False
  rospy.init_node("ardrone2_sim_control")
  rospy.wait_for_service("/gazebo/apply_body_wrench")
  getState = rospy.ServiceProxy("/gazebo/get_model_state",GetModelState)
  setState = rospy.ServiceProxy("/gazebo/set_model_state",SetModelState)
  rospy.Service("/ardrone2/heli", Control, controlCb)
  rospy.Timer(rospy.Duration(1./20),sendControl)
  rospy.spin()

def sendControl(event):
  global getState
  global setState
  global flag
  global roll
  global pitch
  global gaz
  global yaw
  global airborne
  if flag == 4:
    reset = SetModelState()
    reset.pose = Pose()
    #reset.pose.position.x = reset.pose.position.y = reset.pose.position.z = 0
    #reset.pose.orientation.x = reset.pose.orientation.y = reset.pose.orientation.z = 0
    #reset.pose.orientation.w = 1
    reset.twist = Twist()
    reset.model_name = droneName
    reset.reference_frame = "world"
    airborne = False
    setState(reset)
  else:
    curr = getState(droneName,"world")
    print curr
    if flag == 3 and not airborne:
      takeoff(curr)
      airborne = True
    elif flag == 2 and airborne:
      land(curr)
      airborne = False
    elif (flag == 0 or flag == 1) and airborne:
      new = SetModelState()
      new.model_name = droneName
      new.reference_frame = "world"
      new.pose = curr.pose
      # add random movements :)
      new.twist = Twist()
      r,p,currYaw = tf.transformations.euler_from_quaternion([new.pose.orientation.x,new.pose.orientation.y,new.pose.orientation.z,new.pose.orientation.w])
      x = -pitch * controlMult
      y = roll * controlMult
      new.twist.linear.x = x * cos(currYaw) + y * sin(currYaw) 
      new.twist.linear.y = x * sin(currYaw) - y * cos(currYaw) 
      new.twist.linear.z = gaz * controlMult
      new.twist.angular.z = -yaw * controlMult
      new.twist.linear.x += (random.random() - .5)/turbMult
      new.twist.linear.y += (random.random() - .5)/turbMult
      new.twist.linear.z += (random.random() - .5)/turbMult
      new.twist.angular.x += (random.random() - .5)/turbMult
      new.twist.angular.y += (random.random() - .5)/turbMult
      new.twist.angular.z += (random.random() - .5)/turbMult
      setState(new)
      rospy.sleep(.01)


def land(currState):
  new = SetModelState()
  new.model_name = droneName
  new.reference_frame = "world"
  new.pose = currState.pose
  new.twist = Twist()
  new.twist.linear.z = -.4
  setState(new)
  rospy.sleep(.05)
  currState = getState(droneName,"world")
  while(abs(currState.twist.linear.z) > .02):
    currState = getState(droneName,"world")
    print currState
    rospy.sleep(.01)
  new = SetModelState()
  new.model_name = droneName
  new.reference_frame = "world"
  new.pose = currState.pose
  new.twist = Twist()
  setState(new)

def takeoff(currState):
  oldz = currState.pose.position.z 
  new = SetModelState()
  new.model_name = droneName
  new.reference_frame = "world"
  new.pose = currState.pose
  new.twist = Twist()
  new.twist.linear.z = .4
  setState(new)
  while(currState.pose.position.z < 1.0 + oldz):
    currState = getState(droneName,"world")
    rospy.sleep(.01)
  new = SetModelState()
  new.model_name = droneName
  new.reference_frame = "world"
  new.pose = currState.pose
  new.twist = Twist()
  setState(new)

def controlCb(req):
  global getState
  global flag
  global roll
  global pitch
  global gaz
  global yaw
  flag = req.flag
  roll = req.roll
  pitch = req.pitch
  gaz = req.gaz
  yaw = req.yaw
  return Control._response_class()

if __name__ == "__main__":
  main()
