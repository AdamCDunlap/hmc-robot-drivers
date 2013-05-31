#!/usr/bin/env python
import roslib; roslib.load_manifest('kinect_pan')
import rospy
import tf
from dynamixel_msgs import msg


def jcb(data):
  global br
  br.sendTransform((0,0,.04),
      tf.transformations.quaternion_from_euler(0,0,data.current_pos),
      rospy.Time.now(),
      "openni_camera",
      "pan_base")

if __name__ == '__main__':
  global br
  br = tf.TransformBroadcaster()
  rospy.init_node("kinecttf")
  try:
	rospy.wait_for_message("/pan_controller/state",5)
	rospy.Subscriber("/pan_controller/state", msg.JointState,jcb)
	rospy.spin()
  except:
          while not rospy.is_shutdown():
		  br.sendTransform((0,0,.04),
				  tf.transformations.quaternion_from_euler(0,0,0),
				  rospy.Time.now(),
				  "openni_camera",
				  "pan_base") 
		  rospy.sleep(.05)

