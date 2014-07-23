#!/usr/bin/env python
import roslib; roslib.load_manifest('neato_lidar')
import rospy
import cv2
import numpy as np
import sys
import neato_lidar
import neato_lidar.msg
import math

class Data:
    pass
    
D = Data()

def process_ranges():
    

    img = np.zeros((D.imgSize[0], D.imgSize[1], 3), np.uint8)

    for angdeg, dist in enumerate(D.ranges):
        angrad = math.radians(angdeg+180)

        if dist > 0:
            print_dist = dist * 0.05

            endpt = (int(D.imgSizes[0]/2 + math.sin(angrad)*print_dist),
                     int(D.imgSizes[1]/2 + math.cos(angrad)*print_dist))
            cv2.line(img, (D.imgSizes[0]/2, D.imgSizes[1]/2), endpt, 255)

    cv2.imshow('image', img)


def main():
    rospy.init_node('lidar_example')

    cv2.namedWindow('image')
    cv2.moveWindow('image', 400, 0)

    D.ranges = [0]*360

    D.imgSize = (600, 600)

    def change_ranges(d):
        D.ranges = d.ranges
    rospy.Subscriber('lidar', neato_lidar.msg.LidarRanges, change_ranges)

    while True:
        key_press = cv2.waitKey(5) & 255

        process_ranges()

        if key_press == 255:
            pass
        elif key_press == ord('q') or key_press == 27: # if a 'q' or ESC was pressed
            print "quitting..."
            return

if __name__ == "__main__":
    main()

