#!/usr/bin/env python
import roslib; roslib.load_manifest("ardrone2_mudd_gazebo")
import rospy
from gazebo.srv import GetModelState, SetModelState
from ardrone2_mudd.srv import Control,Config
from geometry_msgs.msg import Twist,Pose
from math import cos,sin,pi
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
turbMult = 15

controlMult = 2

maxSpeed = 1.5 # m/s or (?)rad/s
accelXYZ = 6.1 # m/ss
maxR = pi/8
maxP = pi/12

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
  rospy.Service("/ardrone2/config", Config, configCb)
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
    reset.pose.position.x = reset.pose.position.y = reset.pose.position.z = .04
    reset.pose.orientation.x = reset.pose.orientation.y = reset.pose.orientation.z = 0
    reset.pose.orientation.w = 1
    reset.twist = Twist()
    reset.model_name = droneName
    reset.reference_frame = "world"
    airborne = False
    setState(reset)
  else:
    if flag == 3 and not airborne:
      takeoff()
      airborne = True
    elif flag == 2 and airborne:
      land()
      airborne = False
    elif (flag == 0 or flag == 1) and airborne:
      movement(event.last_duration)

def accel(ctrlVal,currSpeed,time):
  desiredSpeed = ctrlVal * maxSpeed
  if currSpeed < desiredSpeed:
    newSpeed = currSpeed + accelXYZ * time
    if newSpeed > desiredSpeed:
      return desiredSpeed
    return newSpeed
  elif currSpeed > desiredSpeed:
    newSpeed = currSpeed - accelXYZ * time
    if newSpeed < desiredSpeed:
      return desiredSpeed
    return newSpeed
  else:
    return currSpeed


def movement(dt):
  global getState
  global setState
  global flag
  global roll
  global pitch
  global gaz
  global yaw
  global airborne
  curr = getState(droneName,"world")
  new = SetModelState()
  new.model_name = droneName
  new.reference_frame = "world"
  new.pose = curr.pose
  # add random movements :)
  new.twist = Twist()
  r,p,currYaw = tf.transformations.euler_from_quaternion([new.pose.orientation.x,new.pose.orientation.y,new.pose.orientation.z,new.pose.orientation.w])
  x = -pitch
  y = roll 
  globalx = x * cos(currYaw) + y * sin(currYaw)
  globaly = x * sin(currYaw) - y * cos(currYaw)
  new.twist.linear.x = accel(globalx,curr.twist.linear.x,dt) 
  new.twist.linear.y = accel(globaly,curr.twist.linear.y,dt) 
  new.twist.linear.z = accel(gaz,curr.twist.linear.z,dt)
  new.twist.angular.z = accel(-yaw,curr.twist.angular.z,dt)
  new.twist.linear.x += (random.random() - .5)/turbMult
  new.twist.linear.y += (random.random() - .5)/turbMult
  new.twist.linear.z += (random.random() - .5)/turbMult
  new.twist.angular.x += (random.random() - .5)/turbMult
  new.twist.angular.y += (random.random() - .5)/turbMult
  new.twist.angular.z += (random.random() - .5)/turbMult
  nqo = calcRP(new)
  new.pose.orientation.x = nqo[0]
  new.pose.orientation.y = nqo[1]
  new.pose.orientation.z = nqo[2]
  new.pose.orientation.w = nqo[3]
  setState(new)
  rospy.sleep(.01)

def calcRP(state):
  r,p,currYaw = tf.transformations.euler_from_quaternion([state.pose.orientation.x,state.pose.orientation.y,state.pose.orientation.z,state.pose.orientation.w])
  x = state.twist.linear.x
  y = state.twist.linear.y
  npitch = (x*cos(currYaw) + y * sin(currYaw))/maxSpeed * maxP
  nroll = (-y*cos(currYaw) + x * sin(currYaw))/maxSpeed * maxR
  return tf.transformations.quaternion_from_euler(nroll,npitch,currYaw)

def land():
  currState = getState(droneName,"world")
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
    rospy.sleep(.01)
  new = SetModelState()
  new.model_name = droneName
  new.reference_frame = "world"
  new.pose = currState.pose
  new.twist = Twist()
  setState(new)

def takeoff():
  currState = getState(droneName,"world")
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

def configCb(req):
  return Config._response_class()

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
