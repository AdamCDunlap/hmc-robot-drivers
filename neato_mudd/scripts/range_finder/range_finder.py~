#!/usr/bin/python
#############################################
##    Range finder GUI for Neato XV11
##    For use at Harvey Mudd College
##    Authors: Cyrus Huang, Zakkai Davidson
##    Date: 6/13/13
##    How it works: check the frontline and turn;
##    the direction depends on whether the left and right line is detected
##    Problem: cannot avoid obstables; not straight when following straight walls
##
#############################################
##    NOTE:
##    Run Neato driver first with
##    rosrun neato_mudd driver.py
#############################################
import roslib; roslib.load_manifest('neato_mudd')
import rospy
import cv
import neato_mudd

from std_msgs.msg import *
from neato_mudd.msg import *
from neato_mudd.srv import *
from math import *

# class for a generic data holder
class Data:
    def __init__(self): pass    # empty constructor

D = Data()

# window variables
WIN_WIDTH  = 600                # keeps square windows
WIN_HEIGHT = WIN_WIDTH


# line drawing variables
MAX_MAG      = 1000             # unreliable data above 10m
MAG_SCALE    = 100              # 100 pixels per meter
CENTER       = WIN_WIDTH/2
ANGLE_OFFSET = 90               # front of robot faces up on screen
REV          = 360              # 360 degrees per rev (range data is stored in degrees)

# OPTIONS
SHOW_HOUGH = False              # set to true to show Hough transformation image


def rangeGUI():
    """ creates and displays a GUI for the range finder data
        Ranges window: shows range finder values as red lines
        coming from the center of the range finder
        HoughLines window: shows the result of using a Hough
        transformation on image containing the range values as points.
    """
    global D
    
    init_GUI() # initialize images and windows

    D.dangerList = [] # Set up the danger point list
    
    # main loop
    while rospy.is_shutdown() == False:

        # loop through every angle
        for angle in range(REV):
            magnitude = MAG_SCALE*D.ranges[angle]
            x = int(CENTER + magnitude*cos(pi/180*(angle+ANGLE_OFFSET)))  # find x and y coordinates based on the angle
            y = int(CENTER - magnitude*sin(pi/180*(angle+ANGLE_OFFSET)))  # and the length of the line

            # put the danger points into the list
            if x > CENTER - 30 and x < CENTER + 30 and y < CENTER -30 and y > CENTER - 90:
                D.dangerList.append((x,y))
                
            if 0 < magnitude < MAX_MAG: # if data is within "good data" range
                # add line to the ranges image
                cv.Line(D.image, (CENTER,CENTER), (x,y), cv.RGB(255, 0, 0))
                # add dot to image being used in Hough transformation
                cv.Line(D.hough, (x,y), (x,y), cv.RGB(255, 0, 0))

        # wait and check for quit request
        key_code = cv.WaitKey(1) & 255
        key_press = chr(key_code)
        if key_code == 27 or key_press == 'q' : # if ESC or 'q' was pressed
            rospy.signal_shutdown( "Quitting..." )

        # find walls and add to image using Hough transformation
        findHoughLines()

        # call wall following algorithm
        # wallFollow()

        # show image with range finder data and calculated walls
        cv.ShowImage("Ranges",  D.image)
        
        # show image used in Hough transformation if option is selected
        if SHOW_HOUGH:
            cv.ShowImage("HoughLines", D.color_dst)

        # clear the images for next loop
        cv.Set(D.image, cv.RGB(0, 0, 0))
        cv.Set(D.hough, cv.RGB(0, 0, 0))

        # clear the danger list for next loop
        D.dangerList = []


    D.tank(0, 0) # stops the robot
    print "Quitting..."
            

            

def init_GUI():
    """ initializes open cv windows and creates images to display """
    global D

    print
    print "Press 'q' in Ranges window to quit"
    
    # create window and image to show range values
    cv.NamedWindow("Ranges")
    cv.MoveWindow("Ranges", WIN_WIDTH/2, WIN_HEIGHT/2)
    D.image = cv.CreateImage((WIN_WIDTH,WIN_HEIGHT), 8, 3) # 8 is pixel depth and 3 is # of channels

    # window for Hough transformation
    if SHOW_HOUGH:
        cv.NamedWindow("HoughLines")
        cv.MoveWindow("HoughLines", WIN_WIDTH/2 + WIN_HEIGHT, WIN_HEIGHT/2)
    # image for Hough transformation
    D.hough = cv.CreateImage((WIN_WIDTH,WIN_HEIGHT), 8, 3) # image used for Hough transformation
    
    # initialize ROS subscription
    rospy.init_node("range_listener", anonymous=True)
    rospy.Subscriber( "laserRangeData", LaserRangeData, range_callback )

    # initialize ROS service
    rospy.wait_for_service('tank') # wait until the motors are available
    D.tank = rospy.ServiceProxy('tank',Tank)
    
    # give initial values to range data before first callback
    D.ranges =[0]*REV


def range_callback(data):
    """ handles published range data and updates global """
    global D

    D.ranges = data.range_data


def findHoughLines():
    """ Uses the Hough transformation to find lines from the sensor
        readings and displays them
    """
    global D

    # initialize lists
    D.lines        = []
    D.theta        = []
    D.distance     = []
    D.midpoint     = []

    # sensitivity options for Hough transformation
    threshold    = 20
    min_line_len = 10
    max_gap_len  = 30
    line_width   = 1
    
    # source for Hough transformation has dots instead of lines
    src = D.hough

    # prepare image and destination for Hough transformation
    dst = cv.CreateImage(cv.GetSize(src), 8, 1)
    D.color_dst = cv.CreateImage(cv.GetSize(src), 8, 3)
    storage = cv.CreateMemStorage(0)
    lines = 0
    cv.Canny(src, dst, 50, 200, 3)
    cv.CvtColor(dst, D.color_dst, cv.CV_GRAY2BGR)

    # apply Hough transformation to find walls
    # For more information, see:
    # http://docs.opencv.org/doc/tutorials/imgproc/imgtrans/hough_lines/hough_lines.html
    lines = cv.HoughLines2(dst, storage, cv.CV_HOUGH_PROBABILISTIC, line_width, \
                           pi / 180, threshold, min_line_len, max_gap_len)

    # draw the danger zone
    cv.Rectangle(D.image, (CENTER - 30,CENTER - 90), (CENTER + 30, CENTER -30), cv.RGB(25,25,112), 2,8)
    
    for line in lines:
        cv.Line(D.color_dst, line[0], line[1], cv.CV_RGB(0, 255, 0), 1, 8)

        # storing the lines and their distances
        D.lines.append((line[0],line[1]))
        x1 = float(line[0][0])
        y1 = float(line[0][1])
        x2 = float(line[1][0])
        y2 = float(line[1][1])
        x3 = float(CENTER)
        y3 = float(CENTER)

        # find the midpoint, the angle, and the distance to center
        midpoint = (int((x1+x2)/2),int((y1+y2)/2))
        theta = atan2((y2-y1),(x2-x1)) / pi * 180

        if (x2 - x1) != 0:
            slope = (y2 - y1) / (x2 - x1)
            intercept = (x2*y1 - x1*y2)/(x2 - x1)
            distance = abs(y3 - slope * x3 - intercept) / sqrt(slope**2 + 1)
        else:
            distance = abs(x2 - x3)
        
        cv.Line(D.image, line[0], line[1], cv.CV_RGB(0, 255, 0), 1, 8)
        cv.Line(D.image, midpoint, midpoint, cv.RGB(255, 255, 255), 4, 8)

        # add data to the list
        D.theta.append(theta)
        D.distance.append(distance)
        D.midpoint.append(midpoint)
    
def wallFollow():
    """ tries to keep the wall lines vertical using arcade control """
    global D
    
    # set up variables and constants
    speed = 250
    k = 1.0
    angle_offset = 15
    distance_offset = 100
    x_sum = 0
    y_sum = 0
    minListNumber = 3

    lineAhead = False
    lineLeft = False
    lineRight = False
    
    try:
        try:
            # find the average x coordinate of all danger points
            for point in D.dangerList:
                x_sum += point[0]
                y_sum += point[1]
            x_avg = x_sum / len(D.dangerList)
            y_avg = y_sum / len(D.dangerList)
        except:
            pass

        # check all the hough lines and put flags
        for i in range(len(D.midpoint)):
            line_midpoint = D.midpoint[i]
            line_distance = D.distance[i]
            line_theta = D.theta[i]
            line_x = (D.lines[i][0][0],D.lines[i][1][0])
            line_y = (D.lines[i][0][1],D.lines[i][1][1])

            if abs(line_theta) < angle_offset:
                if line_midpoint[1] > CENTER + distance_offset:
                    lineBehind = True
                elif line_midpoint[1] < CENTER and line_midpoint[1] > distance_offset and max(line_x) > CENTER and min(line_x) < CENTER:
                    lineAhead = True
            elif abs(line_theta) >= (90 - angle_offset):
                if line_x[0] < CENTER and line_x[1] < CENTER and max(line_y) < CENTER:
                    lineLeft = True
                elif line_x[0] > CENTER and line_x[1] > CENTER and max(line_y) < CENTER:
                    lineRight = True

        # decide how to tank
        if lineAhead:
            if lineRight:
                print "turn left"
                D.tank(-100,100)
                sleep(0.75)
            else:
                print "turn right"
                D.tank(100,-100)
                sleep(0.75)
                
        elif len(D.dangerList) > minListNumber:
            delta_p = (70 - abs(CENTER - 30 - y_avg))
            if x_avg > CENTER + 5:
                print "danger right"
                D.tank(100 - delta_p,200 + delta_p)
            elif x_avg < CENTER - 5:
                print "danger left"
                D.tank(200 + delta_p,100 - delta_p)
            
        else:
            print "go ahead"
            theta = 0
            for thetas in D.theta:
                if abs(thetas) > abs(theta):
                    theta = thetas
            delta = 90 - abs(theta)
            print theta
            if theta > 0:
                D.tank(speed - delta, speed + delta)
            else:
                D.tank(speed + delta ,speed - delta)

    except:
        pass

##    print lineBehind,lineAhead
##    print lineLeft,lineRight

    
    

if __name__ == "__main__":
    rangeGUI()

