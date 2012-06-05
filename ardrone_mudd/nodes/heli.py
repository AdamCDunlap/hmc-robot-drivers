USE_DRONE = True

if(USE_DRONE):
  import roslib; roslib.load_manifest('ardrone_mudd')
  from ardrone_mudd.srv import *
  from ardrone_mudd.msg import *
  import rospy
import time,sys,random

class FakeData:
  altitude = 542
  vx = 3
  vy = 4
  vz = 0
  phi = 100
  theta = 4242
  psi = 3064
  state = 789

def navDataUpdate(data):
  global commands
  global lastsent
  global helistr
  sys.stdout.write("\r\t [alt: %i] \t [phi: %i psi: %i theta: %i] \t [vx: %i vy: %i vz: %i] \t state: %i \n" \
      %
      (data.altitude,data.phi,data.psi,data.theta,data.vx,data.vy,data.vz,0))
  sys.stdout.write("\rLast sent: %s\n" % (lastsent))
  sys.stdout.write("\033[A")
  sys.stdout.write("\033[A")
  sys.stdout.flush()

  sflag = 0
  sphi = 0
  stheta = 0
  sgaz = 0
  syaw = 0
  sgaz = 0 # (542 - data.altitude)/542

  helistr = "heli %i %.3f %.3f %.3f %.3f" \
    % (sflag,sphi,stheta,sgaz,syaw)
  heli(helistr)
  lastsent = helistr

def videoUpdate(data):
    test = 0

def main():
  global heli
  global lastsent
  lastsent = "none"
  if(USE_DRONE):
    rospy.init_node("drone_kb_control",log_level=rospy.DEBUG)
    print "Connecting to droneControl service"
    rospy.wait_for_service("droneControl")
    heli = rospy.ServiceProxy("droneControl", Control) #add persistent
    print "\r Connecting to navData service"
    #rospy.wait_for_service("navData")
    print "test"
    rospy.Subscriber("navData",navData, navDataUpdate, queue_size=1)
    print "\r Connected to services\n"
    rospy.spin()
  #else:
  #  fd = FakeData()
  #  def heli(command):
  #    commands = command.split()
  #    fd.altitude += 40 * float(commands[4])
  #  print "USE_DRONE SET TO FALSE"
  #  while True:
  #    navDataUpdate(fd)
  #    if random.randint(0,1):
  #      fd.altitude += random.randint(-10,10)
  #    time.sleep(.05)
    

if __name__ == "__main__":
  main()
