import roslib; roslib.load_manifest('ardrone2_mudd')
from ardrone2_mudd.srv import *
from ardrone2_mudd.msg import *
from std_msgs.msg import String
import rospy
import cv, math, random, sys

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
    3: print battery level              4: do a front flip
    5: do a back flip                   6: do a left barrel roll
    7: do a right barrel roll

    q: forward left strafe  w: forward  e: forward right strafe
    a: strafe left          s: hover    d: strafe right
    z: backward left strafe x: backward e: backward right strafe

    left arrow:  spin left
    right arrow: spin right
    up arrow:    up
    down arrow:  down
    """
    

    self.lastSent = "None"
    self.airborne = False

    # Camera Sources
    self.cameraSources = {0: "front camera", 1: "ground camera"}
    self.setCam()

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
    self.phi       = math.radians(data.phi/1000.0)
    self.psi       = math.radians(data.psi/1000.0)
    self.theta     = math.radians(data.theta/1000.0)
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
    #self.send(2,0,0,0,0)
    self.hover
    #rospy.sleep(0.5)
    self.send(2,0,0,0,0)
    
  def reset(self):
    self.airborne = False
    self.send(4,0,0,0,0)

  def frontFlip(self):
    print "%sI'm doing a front flip!!!" % self.aLittleExcitement()
    self.configSend("anim 16")

  def backFlip(self):
    print "%sI'm doing a back flip!!!" % self.aLittleExcitement()
    self.configSend("anim 17")

  def leftBarrelRoll(self):
    print "%sI'm rolling left!!!" % self.aLittleExcitement()
    self.configSend("anim 18")

  def rightBarrelRoll(self):
    print "%sI'm rolling right!!!" % self.aLittleExcitement()
    self.configSend("anim 19")

  def aLittleExcitement(self):
    if random.random() < 0.33:
      return "Wheeeee!!!! "
    elif random.random() < 0.5:
      return "Look at me go!!!!! "
    else:
      return ""

  def getKeyPress(self, time = ()):
    if type(time) != tuple:
      time = (time,)
    char = chr(cv.WaitKey(*time) % 255)
    self.keyCmd(char)
    return char

  def keyCmd(self,char):
    #The line below is useful if ever picking new keys. 
    #print ord(char)
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
            elif char == chr(83): #right arrow key
                syaw = self.keyPower
            elif char == chr(81): #left arrow key
                syaw = -self.keyPower
            elif char == chr(82): #down arrow key
                sgaz = self.keyPower
            elif char == chr(84): #up arrow key
                sgaz = -self.keyPower
            elif char == '4':
                self.frontFlip()
            elif char == '5':
                self.backFlip()
            elif char == '6':
                self.leftBarrelRoll()
            elif char == '7':
                self.rightBarrelRoll()

        self.send(sflag, sphi, stheta, sgaz, syaw)

if __name__ == "__main__":
  controller = Ardrone()
  while True:
    controller.getKeyPress()
  
