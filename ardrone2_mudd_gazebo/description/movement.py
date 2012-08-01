import roslib; roslib.load_manifest("ardrone2_mudd_gazebo")
import rospy

def main():
  rospy.wait_for_service("/gazebo/apply_body_wrench")
  getState = rospy.ServiceProxy("/gazebo/get_model_state",GetModelState)
  print getState("my_drone","world")



if __name__ == "__main__":
  main()
