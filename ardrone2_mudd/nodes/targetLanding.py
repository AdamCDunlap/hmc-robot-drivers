#########################################
#########     Drone Imports     #########
#########################################
import roslib; roslib.load_manifest('ardrone2_mudd')
from ardrone2_mudd.srv import *
from ardrone2_mudd.msg import *
from sensor_msgs.msg import *
from std_msgs.msg import String
import rospy
import ardrone2

#########################################
#########  Imports other things #########
#########################################
import time,sys,random,cv,cv_bridge,math

IMAGE_SOURCE = "imageData"

class myArdrone(ardrone2.Ardrone):
    def __init__(self):
        ardrone2.Ardrone.__init__(self)
        self.toleranceArea = 0.05
        self.state = "keyboard"
        self.noBox = True
        self.tracking = False
        self.vertMult = 0.5
        self.strafeMult = 0.5
        self.altMult = 1.0
        self.setCam(1) # Setting downard camera

    def loop(self):
        while True:
            char = self.getKeyPress()
            if char == 'n':
                self.state = "start"
                self.tracking = True
                self.trackingBrain()
            elif self.tracking and not self.noBox:
                self.trackingBrain()

    def trackingBrain(self,timer_event=None):
        if height > 0.85:
            self.land
            self.tracking = False
        dist = math.sqrt(self.centerX**2 + self.centerY**2)
        downPower = self.altMult/(1.0 + dist)
        leftRightPower = (self.centerX - .5) * 2.0 * self.strafeMult
        forwardBackPower = (self.centerY - .5) * 2.0 * self.vertMult
        self.forward(forwardBackPower)
        self.strafeRight(leftRightPower)
        self.down(downPower)
        
       
    def bBoxUpdate(self, data):
        #Format is: "CenterX (in percent of box width) CenterY (in percent of box height)
        #            Area (in percent of box area) LeftEdge (in percent of box width)
        #            TopEdge (in percent of box height) RightEdge (in percent of box width)
        #            BottomEdge (in percent of box height)"
        br           = data.data.split()
        self.centerX = float(br[0])
        self.centerY = float(br[1])
        self.area    = float(br[2])
        self.height  = float(br[6])-float(br[4]) #the y axis points down.
        if self.area < self.toleranceArea:
            print "I see a too small box of area %f" % self.area
            self.noBox = True
        else:
            self.noBox = False

if __name__== "__main__":
  drone = myArdrone()
  print "\r Connecting to bounding box data"
  rospy.Subscriber(IMAGE_SOURCE,String,drone.bBoxUpdate,queue_size=1)
  print "Ready"
  drone.loop()
