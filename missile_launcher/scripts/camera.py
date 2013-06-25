import roslib; roslib.load_manifest('missile_launcher')
import rospy
import cv
from missile_launcher.srv import *
from thunder_launcher import Launcher

from cv_bridge import CvBridge#, CvBridgeError

# create empty global to contain data
class Data():
   def __init__(self): pass

D = Data()

def init_camera():
    """ initialize openCV window and camera """
    global D
    
    print "Initializing camera..."
    cv.NamedWindow("image")
    D.bridge = CvBridge()
    D.camera = cv.CaptureFromCAM(-1)

    

def camera_loop():
    """ main loop to update camera image """
    global D
    
    while rospy.is_shutdown() == False:

        # capture image and 
        D.image = cv.QueryFrame(D.camera)
        cv.ShowImage("image",D.image)

        
        # Get incoming key events using cv.WaitKey (lowest 8 bits)
        key_code = cv.WaitKey(5) & 255 # gets the window's next key_code
        if key_code == 255: continue    # 255 means "no key pressed"
        key_press = chr(key_code)       # convert key_code to a character
        
        if key_code == 27 or key_press == 'q' : # if ESC or 'q' was pressed
            pub.publish(String('q')) # publish the string 'q' either way
            rospy.signal_shutdown( "Quitting..." )
            
if __name__=="__main__":
    init_camera()
    camera_loop()
