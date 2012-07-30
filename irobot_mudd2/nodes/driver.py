#!/usr/bin/python
import roslib; roslib.load_manifest('irobot_mudd')
import rospy
from time import sleep
import create
from threading import Thread
from math import sin,cos,pi
from datetime import datetime

from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.broadcaster import TransformBroadcaster

from irobot_mudd.msg import SensorPacket
from irobot_mudd.srv import *

import cmd,sys,signal,os,serial

class CreateDriver:
    def __init__(self,port):
      self.create = create.Create(port)
      self.create.playSong(((70,8),(72,8),(68,8),(56,8),(63,8)))
      self.packetPub = rospy.Publisher('~sensorData', SensorPacket)
      self.odomPub = rospy.Publisher('/odom',Odometry)
      self.odomBroadcaster = TransformBroadcaster()
      self.fields = ['wheeldropCaster','wheeldropLeft','wheeldropRight','bumpLeft','bumpRight','wall','cliffLeft','cliffFronLeft','cliffFrontRight','cliffRight','virtualWall','infraredByte','advance','play','distance','angle','chargingState','voltage','current','batteryTemperature','batteryCharge','batteryCapacity','wallSignal','cliffLeftSignal','cliffFrontLeftSignal','cliffFrontRightSignal','cliffRightSignal','homeBase','internalCharger','songNumber','songPlaying','x','y','theta','chargeLevel']
      self.then = datetime.now() 
      self.dist  = 0
      self.theta = 0
      self.x     = 0
      self.y     = 0
      self.last = rospy.Time.now()
      self.baseFrame = rospy.get_param("~base_frame","/base_link")
      self.odomFrame = rospy.get_param("~odom_frame","/odom")

    def odomUpdate(self,timer):
      ddist = self.create.getSensor('DISTANCE') / 1000.0
      dth   = self.create.getSensor('ANGLE') * pi/180.0

      self.dist  += ddist
      self.theta += dth

      if (ddist != 0):
        dx = cos(dth)*ddist
        dy = -sin(dth)*ddist
        self.x += (cos(self.theta)*dx - sin(self.theta)*dy)
        self.y += (sin(self.theta)*dx + cos(self.theta)*dy)

      quaternion = Quaternion()
      quaternion.x = 0.0 
      quaternion.y = 0.0
      quaternion.z = sin(self.theta/2)
      quaternion.w = cos(self.theta/2)

      self.odomBroadcaster.sendTransform(
          (self.x, self.y, 0), 
          (quaternion.x, quaternion.y, quaternion.z, quaternion.w),
          rospy.Time.now(),
          self.baseFrame,
          self.odomFrame
          )

      odom = Odometry()
      odom.header.stamp = rospy.Time.now()
      odom.header.frame_id = self.odomFrame
      odom.pose.pose.position.x = self.x
      odom.pose.pose.position.y = self.y
      odom.pose.pose.position.z = 0
      odom.pose.pose.orientation = quaternion

      odom.child_frame_id = self.baseFrame
      if timer.last_duration:
        odom.twist.twist.linear.x = ddist / timer.last_duration
        odom.twist.twist.linear.y = 0
        odom.twist.twist.angular.z = dth / timer.last_duration

      self.odomPub.publish(odom)


    #def sense(self):
    #    now = datetime.now()
    #    elapsed = now - self.then
    #    self.then = now
    #    elapsed = float(elapsed.seconds) + elapsed.microseconds/1000000.
    #    d = self.create.d_distance / 1000.
    #    th = self.create.d_angle*pi/180
    #    dx = d / elapsed
    #    dth = th / elapsed

    #    if (d != 0):
    #        x = cos(th)*d
    #        y = -sin(th)*d
    #        self.x = self.x + (cos(self.th)*x - sin(self.th)*y)
    #        self.y = self.y + (sin(self.th)*x + cos(self.th)*y)

    #    if (th != 0):
    #        self.th = self.th + th

    #    quaternion = Quaternion()
    #    quaternion.x = 0.0 
    #    quaternion.y = 0.0
    #    quaternion.z = sin(self.th/2)
    #    quaternion.w = cos(self.th/2)

    #    self.odomBroadcaster.sendTransform(
    #        (self.x, self.y, 0), 
    #        (quaternion.x, quaternion.y, quaternion.z, quaternion.w),
    #        rospy.Time.now(),
    #        "base_link",
    #        "odom"
    #        )

    #    odom = Odometry()
    #    odom.header.stamp = rospy.Time.now()
    #    odom.header.frame_id = "odom"
    #    odom.pose.pose.position.x = self.x
    #    odom.pose.pose.position.y = self.y
    #    odom.pose.pose.position.z = 0
    #    odom.pose.pose.orientation = quaternion

    #    odom.child_frame_id = "base_link"
    #    odom.twist.twist.linear.x = dx
    #    odom.twist.twist.linear.y = 0
    #    odom.twist.twist.angular.z = dth

    #    self.odomPub.publish(odom)


    #    packet = SensorPacket()
    #    for field in self.fields[:-4]:
    #        packet.__setattr__(field,self.create.__getattr__(field))

    #    self.chargeLevel = float(packet.batteryCharge) / float(packet.batteryCapacity)
    #    packet.__setattr__('x',self.x)
    #    packet.__setattr__('y',self.y)
    #    packet.__setattr__('theta',self.th)
    #    packet.__setattr__('chargeLevel',self.chargeLevel)
    #    self.packetPub.publish(packet)

    #    if packet.homeBase:
    #        self.inDock = True
    #    else:
    #        self.inDock = False

    #def circle(self,req):
    #    self.create.forwardTurn(req.speed,req.radius)
    #    return CircleResponse(True)

    def demo(self,req):
        self.create.demo(req.demo)
        return DemoResponse(True)

    def leds(self,req):
        self.create.leds(req.color,req.intensity,req.play,req.advance)
        return LedsResponse(True)

    def tank(self,req):
        self.create.driveDirect(req.left,req.right)
        return TankResponse(True)

    #def turn(self,req):
    #    if (req.clear):
    #        self.create.clear()
    #    self.create.turn(req.turn)
    #    return TurnResponse(True)

    #def dock(self,req):
    #    """ req.charge = 0: dock and charge 
    #                   = 1: wake up from charging
    #                   = 2: dock and wake up immediately """

    #    if req.charge == 2:
    #        self.create.restart()
    #        return DockResponse(True)

    #    self.create.brake()
    #    self.create.demo(1)
    #    while(not self.inDock):
    #        pass
    #    
    #    if req.charge == 0:
    #        rospy.sleep(3)
    #        self.create.restart()
    #    return DockResponse(True)

    def opCode(self,opCode):
        self.create.send(opCode)

    def twist(self,req):
        x = req.linear.x*1000.
        th = req.angular.z
        self.create.go(x,th)
    #    if (x == 0):
    #        th = th*180/pi
    #        speed = (8*pi*th)/9
    #        self.create.left(int(speed))
    #    elif (th == 0):
    #        x = int(x)
    #        self.create.driveDirect(x,x)
    #    else:
    #        self.create.forwardTurn(int(x),int(x/th))

    def song(self,req):
      song = zip(req.notes,req.durations)
      for x in xrange(0, len(song), 16):
        self.create.playSong(song[x:x+16])
        sleep( sum( req.durations[x:x+16])/64.0)
      return SongResponse(True)

class prompt(cmd.Cmd):
    def __init__(self,robot):
        cmd.Cmd.__init__(self)
        self.prompt = '>>: '
        self.robot = robot.create
        self.robotWrap = robot
        self.intro = "\nReady!\nEnter help for commands"

    def do_quit(self,line):
        """ Attempts to stop and quit the program """
        self.quit()

    def do_status(self,line):
        """ Prints the status of the robot """
        print """
        Battery: %f
        X: %f.3   Y: %f.3 Th: %f.3
        Last tank command: %s
        Serial status: %s
        """ % (self.robotWrap.chargeLevel,self.robotWrap.x,self.robotWrap.y \
                ,self.robotWrap.th,self.robot.lastTank,self.robot.port)

    def do_stop(self,line):
        """ Executes tank 0 0 """
        print "Trying to stop the robot"
        self.robot.tank(0,0)

    def do_tank(self,line):
        """ Executes tank LEFT RIGHT """
        lineS = line.split()
        try:
            left = int(lineS[0])
            right = int(lineS[1])
            self.robot.driveDirect(left,right)
        except:
            print "Invalid arguments " + line

    def do_reset(self,line):
        """ Reset the robot """
        self.robot.reset()

    def quit(self,*args):
        print "\nTrying to quit gracefully, if all else fails try ctrl-\\"
        rospy.core.signal_shutdown('keyboard interrupt')
        self.robot.shutdown()
        sys.exit(0)

if __name__ == '__main__':
    print "Starting..."
    node = rospy.init_node('irobot_mudd')
    port = rospy.get_param('~port', "/dev/ttyUSB0")
    rate = rospy.get_param('~odom_rate', 15)

    if(not os.path.exists(port)):
        print rospy.resolve_name('~port')

        print """\n        Port: %s does not exist
        Make sure bluetooth is setup or serial cable is plugged in
        Finally run 'rosparam set /irobot_mudd/port PORT' where port is your port
        such as /dev/ttyUSB0   /dev/rfcomm0

        Bluetooth reminders: 
            hcitool scan                          Get your hex address
            sudo rm /dev/rfcomm0                  Remove the port
            sudo rfcomm connect 0 HEXADDRESS 1    Connect
        """ % (port)
        sys.exit(0)

    print "Connecting to robot"
    driver = CreateDriver(port)
    
    print "Connecting to ROS"
    #rospy.Service('~circle',Circle,driver.circle)
    rospy.Service('~demo',Demo,driver.demo)
    rospy.Service('~leds',Leds,driver.leds)
    rospy.Service('tank',Tank,driver.tank)
    #rospy.Service('~turn',Turn,driver.turn)
    #rospy.Service('~dock',Dock,driver.dock)
    rospy.Service('~song',Song,driver.song)

    rospy.Subscriber("cmd_vel", Twist, driver.twist)

    prompt = prompt(driver)
    signal.signal(signal.SIGINT,prompt.quit)

    print "Starting sensor polling"
    if driver.create.sensorDataIsOK():
      rospy.Timer(rospy.Duration(1.0/rate),driver.odomUpdate)
      try:
          prompt.cmdloop()
      except serial.SerialException:
          print "\n Lost connection to robot! \n"
          prompt.quit()
    else:
      print "Could not poll sensors"

        

