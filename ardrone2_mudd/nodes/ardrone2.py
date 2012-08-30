import roslib; roslib.load_manifest('ardrone2_mudd')
from ardrone2_mudd.srv import *
from ardrone2_mudd.msg import *
from std_msgs.msg import String
import rospy
import cv
import math
import sys

#############################################
####   Same as "ardrone.py", but with    ####
####   some tweaks to make it work well  ####
####   with Drone 2.0                    ####
#############################################

class Ardrone():
  def __init__(self,controlName="ardrone2/heli", navPubName="ardrone2/navData", configName="ardrone2/config"):
    rospy.init_node("ArdroneBase")
    print "Connecting to droneControl service"
    rospy.wait_for_service(controlName)
    self.heli = rospy.ServiceProxy(controlName, Control, persistent=True)
    print "\r Connecting to config service"
    rospy.wait_for_service('ardrone2/config')
    self.config = rospy.ServiceProxy(configName, Config)
    print "\r Connected to services"

    print "\r Subscribing to navData"
    rospy.Subscriber(navPubName, navData, self.navDataUpdate, queue_size=1)
    print "\r Subscribed to navData"
    
    print """
    Keyboard Controls:
    h: quit
    t: takeoff              r: reset    enter/return(space): land
    1: use forward camera               2: use bottom camera

    q: forward left strafe  w: forward  e: forward right strafe
    a: strafe left          s: hover    d: strafe right
    z: backward left strafe x: backward e: backward right strafe

    f: spin left
    g: spin right
    v: up
    b: down
    """
    

    self.lastSent = "None"
    self.airborne = False

    # Camera Sources
    self.cameraSources = {0: "front camera", 1: "ground camera"}

    # Navdata fields (partial)
    self.altitude  = 0 
    self.phi       = 0 
    self.psi       = 0 
    self.theta     = 0 
    self.vx        = 0 
    self.vy        = 0 
    self.vz        = 0 
    self.batLevel  = 0 
    self.ctrlState = 0

    # Base speed for drone.
    self.keyPower = .5

    # Reset the drone !!
    self.send(4,0,0,0,0)

    # The Opencv Windows
    cv.NamedWindow('control')
    cv.MoveWindow('control', 1260, 20)

    print "Ready"

  def navDataUpdate(self,data):
    self.altitude  = data.altitude
    self.phi       = data.phi
    self.psi       = data.psi
    self.theta     = data.theta
    self.vx        = data.vx
    self.vy        = data.vy
    self.vz        = data.vz
    self.batLevel  = data.batLevel
    self.ctrlState = data.ctrlState

  def printStatus(self):
    print "\t [alt: %i] \t [phi: %i psi: %i theta: %i] \t [vx: %i vy: %i vz: %i] \t [bat: %i  state: %i]" \
      % (self.altitude,self.phi,self.psi,self.theta,self.vx,self.vy,self.vz,self.batLevel,self.ctrlState)
    print "\t Last sent: %s" % (self.lastsent)

  def configSend(self, configStr):
    self.lastConfigSent = configStr
    self.config(configStr)

  def setCam(self, camNum = 0):
    self.cameraNumber = camNum
    print "Setting camera source to %s " % self.cameraSources[self.cameraNumber]
    self.configSend("camera %i" % self.cameraNumber)

  def send(self,flag,phi,theta,gaz,yaw):
    self.lastsent = flag,phi,theta,gaz,yaw
    self.heli(flag,phi,theta,gaz,yaw)    
    #rospy.sleep(1.0)

  def spinLeft(self,power):
    self.send(0,0,0,0,-power)

  def spinRight(self,power):
    self.send(0,0,0,0,power)

  def strafeRight(self,power):
    self.send(1,power,0,0,0)

  def strafeLeft(self,power):
    self.send(1,-power,0,0,0)

  def forward(self,power):
    self.send(1,0,-power,0,0)

  def backward(self,power):
    self.send(1,0,power,0,0)

  def up(self,power):
    self.send(0,0,0,power,0)

  def down(self,power):
    self.send(0,0,0,-power,0)

  def hover(self):
    self.send(0,0,0,0,0)

  def takeoff(self):
    if not self.airborne:
      print "takeoff"
      self.airborne = True
      self.send(3,0,0,0,0)
      rospy.sleep(1)
      self.hover()

  def land(self):
    self.airborne = False
    self.hover
    rospy.sleep(0.5)
    self.send(2,0,0,0,0)
    
  def reset(self):
    self.airborne = False
    self.send(4,0,0,0,0)

  def getKeyPress(self, time = ()):
    if type(time) != tuple:
      time = (time,)
    char = chr(cv.WaitKey(*time) % 255)
    self.keyCmd(char)
    return char

  def keyCmd(self,char):
    if char == chr(254):
        return
    elif char == ' ':
        self.land() # Landing
    elif char == 'h':
        self.land() # Landing
        sys.exit(0)
    elif char == 'r':
        self.reset() # Resetting
    elif char == 't':
        self.takeoff() # Take Off
    elif char == '1':
        self.setCam()
    elif char == '2':
        self.setCam(1)
    elif char == "3":
        print "Battery Level", self.batLevel
    elif self.airborne:
        sflag  = 1 
        sphi   = 0
        stheta = 0
        sgaz   = 0
        syaw   = 0
        sgaz   = 0
        if char == 'w':
            stheta = -self.keyPower
        elif char == 'x':
            stheta = self.keyPower
        elif char == 'a':
            sphi = -self.keyPower  
        elif char == 'd':
            sphi = self.keyPower  
        elif char == 'e':
            stheta = -math.sqrt(self.keyPower/2)
            sphi = math.sqrt(self.keyPower/2)  
        elif char == 'z':
            stheta = math.sqrt(self.keyPower/2)
            sphi = -math.sqrt(self.keyPower/2)  
        elif char == 'q':
            stheta = -math.sqrt(self.keyPower/2)
            sphi = -math.sqrt(self.keyPower/2)  
        elif char == 'c':
            stheta = math.sqrt(self.keyPower/2)
            sphi = math.sqrt(self.keyPower/2)  
        else:
            sflag = 0
            if char == 's': #Self-adjusting hover
                sflag = 0
            elif char == '0': #Non-adjusting hover
                sflag = 1
            elif char == 'g':
                syaw = self.keyPower
            elif char == 'f':
                syaw = -self.keyPower
            elif char == 'v':
                sgaz = self.keyPower
            elif char == 'b':
                sgaz = -self.keyPower
            elif char == '4':
                self.configSend("anim 16")
            elif char == '5':
                self.configSend("anim 17")
            elif char == '6':
                self.configSend("anim 18")
            elif char == '7':
                self.configSend("anim 19")

        self.send(sflag, sphi, stheta, sgaz, syaw)

if __name__ == "__main__":
  controller = Ardrone()
  while True:
    controller.getKeyPress()
  
