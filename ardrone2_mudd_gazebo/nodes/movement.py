import roslib; roslib.load_manifest("ardrone2_mudd_gazebo")
import rospy
from gazebo.srv import GetModelState, SetModelState
from ardrone2_mudd.srv import Control
from geometry_msgs.msg import Twist,Pose
from math import cos,sin
import tf

getState = 0
setState = 0
flag = 0
roll = 0
pitch = 0
gaz = 0
yaw = 0
def main():
  global getState
  global setState
  global flag
  global roll
  global pitch
  global gaz
  global yaw
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
  if flag == 4:
    reset = SetModelState()
    reset.pose = Pose()
    #reset.pose.position.x = reset.pose.position.y = reset.pose.position.z = 0
    #reset.pose.orientation.x = reset.pose.orientation.y = reset.pose.orientation.z = 0
    #reset.pose.orientation.w = 1
    reset.twist = Twist()
    reset.model_name = "my_drone"
    reset.reference_frame = "world"
    setState(reset)
  else:
    curr = getState("my_drone","world")
    print curr.pose
    new = SetModelState()
    new.model_name = "my_drone"
    new.reference_frame = "world"
    new.pose = curr.pose
    r,p,currYaw = tf.transformations.euler_from_quaternion([new.pose.orientation.x,new.pose.orientation.y,new.pose.orientation.z,new.pose.orientation.w])
    print r,p,currYaw
    x = -pitch
    y = roll
    new.twist = Twist()
    new.twist.linear.x = x * cos(currYaw) + y * sin(currYaw) 
    new.twist.linear.y = x * sin(currYaw) - y * cos(currYaw) 
    new.twist.linear.z = gaz
    new.twist.angular.z = -yaw
    setState(new)
    rospy.sleep(.01)



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
