#!/usr/bin/python
import roslib; roslib.load_manifest('neato_lidar')
import rospy
import neato_lidar.msg

import serial

########################################################
# ROS wrapper for the Neato XV11 robot's lidar sensor.
# Author: Adam Dunlap
# Date: 7/10/2014
# ROS Version: Groovy
########################################################

class Checksum:
    """Calculates a running checksum for the LIDAR"""
    def __init__(self):
        """Initializes"""
        self.checksum = 0
        self.on_high_byte = False
        self.low_byte = 0
    def add(self, byte):
        """Add a byte to the checksum"""
        if not self.on_high_byte:
            self.low_byte = byte
        else:
            self.checksum = (self.checksum << 1) + \
                            (self.low_byte | (byte << 8) )
        self.on_high_byte = not self.on_high_byte
    def reset(self):
        """Reset the sum"""
        self.checksum = 0
    def get(self):
        """Return the calculated sum"""
        return ((self.checksum & 0x7FFF) + (self.checksum >> 15)) & 0x7FFF
    def check(self, wantedsum):
        """Checks whether this sum is equal to the given sum, then resets"""
        s = self.get()
        self.reset()
        return s == wantedsum

class LidarReader:
    def __init__(self, serial_connection, publisher):
        self.serial_connection = serial_connection
        self.ranges = [0 for _ in range(360)]
        self.strengths = [0 for _ in range(360)]
        self.publisher = publisher

    def read_dists(self):
        """Runs a loop that computes distances"""

        state = 'wait_for_start'
        checksum = Checksum()


        while True:
            byte = ord(self.serial_connection.read(1))
            if state == 'wait_for_start':
                if byte == 0xFA:
                    # Start byte
                    state = 'reading'
                    bytenum = 1 # 0th byte was start byte
                    checksum.add(byte)

            elif state == 'reading':
                if bytenum < 20:
                    checksum.add(byte)

                if bytenum == 1:
                    # Index
                    idx = byte - 0xA0

                    if idx < 0 or idx >= 90:
                        state = 'wait_for_start'

                elif bytenum == 2:
                    # Speed low byte
                    spdlowbyte = byte
                elif bytenum == 3:
                    # Speed high byte
                    spd = spdlowbyte | (byte << 8)

                    #print 'spd is', spd
                    if spd < 11520:
                        print 'Speed is probably too low to send valid data.',
                        print 'Change the battery.'


                elif bytenum == 20:
                    # Checksum low byte
                    calcdsum = byte
                elif bytenum == 21:
                    # Checksum high byte
                    calcdsum |= byte << 8
                    
                    # Check checksum
                    if not checksum.check(calcdsum):
                        print 'checksum failed'

                    # Publish ranges!
                    ranges = neato_lidar.msg.LidarRanges()
                    ranges.__setattr__("ranges", self.ranges)
                    ranges.__setattr__("strengths", self.strengths)
                    self.publisher.publish(ranges)

                    # we're done with this packet
                    state = 'wait_for_start'

                # Data bytes
                elif ( bytenum % 4 )  == 0:
                    # Byte 0 of data (distance low byte)
                    rangelowbyte = byte
                elif ( bytenum % 4 )  == 1:
                    # Byte 1 of data
                    #(<"invalid data" flag><"strength warning" flag>
                    # <distance 13:8>)
                    if (byte & 0x80) != 0: # high bit is 1
                        invalid = True
                    else:
                        invalid = False
                    if (byte & 0x40) != 0: # second-to-high bit is 1
                        strength_warning = True
                    else:
                        strength_warning = False
                    if invalid:
                        self.ranges[4*idx + bytenum/4 - 1] = 0
                    else:
                        self.ranges[4*idx + bytenum/4 - 1] = \
                                rangelowbyte | ((byte & 0x3F) << 8)
                        # Ranges are in meters
                elif ( bytenum % 4 ) == 2:
                    # Byte 2 of data (signal strength low byte)
                    strengthlowbyte = byte
                elif ( bytenum % 4 ) == 3:
                    self.strengths[4*idx + bytenum/4 - 1] = \
                            strengthlowbyte | ( byte << 8)
                bytenum += 1

if __name__ == '__main__':

    print "Connecting to ROS"
    
    node = rospy.init_node('neato_lidar')

    lidar_pub = rospy.Publisher('lidar', neato_lidar.msg.LidarRanges)

    print "Connecting to LIDAR"



    serial_connection = None
    for i in range(10):
        try:
            port = "/dev/ttyUSB" + str(i)
            serial_connection = serial.Serial(port,115200)
        except:
            pass
        else:
            print "The port is", port

    if not serial_connection:
        print 'Unable to find neato lidar (make sure you have permission to', \
              "access the serial port if it's plugged in!)"
    else:
        print 'connection successful'
        lr = LidarReader(serial_connection, lidar_pub)
        lr.read_dists()
