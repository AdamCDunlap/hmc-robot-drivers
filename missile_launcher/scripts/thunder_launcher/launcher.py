## Driver for the Dream Cheeky Thunder missile launcher using ROS services.
## Part of this code is adapted from the Robot Reasoning Lab 8 at
## https://www.cs.hmc.edu/twiki/bin/view/Robotics/RobotReasoningLab8in2012
## which has been editted by Chris Eriksen
## Author: Zakkai Davidson
## Date: 5/28/13
## This code is the property of Harvey Mudd College, Claremont, California

import time
import os
import sys
import usb.core

# int arrays to write to missile launcher
CODE_UP = [0x02,0x02,0x00,0x00,0x00,0x00,0x00,0x00]
CODE_DOWN = [0x02,0x01,0x00,0x00,0x00,0x00,0x00,0x00]
CODE_LEFT = [0x02,0x04,0x00,0x00,0x00,0x00,0x00,0x00]
CODE_RIGHT = [0x02,0x08,0x00,0x00,0x00,0x00,0x00,0x00]
CODE_STOP = [0x02,0x20,0x00,0x00,0x00,0x00,0x00,0x00]
CODE_FIRE = [0x02,0x10,0x00,0x00,0x00,0x00,0x00,0x00]


# class for controlling the launcher
class Launcher():
    
    def __init__(self):
        self.connect();

    def connect(self):
        """ connects to the launcher """
        self.launcher = usb.core.find(idVendor=0x2123, idProduct=0x1010)
        if self.launcher is None:
            raise ValueError('Launcher not found.')
        if self.launcher.is_kernel_driver_active(0) is True:
            self.launcher.detach_kernel_driver(0)
        self.launcher.set_configuration()
      
    def send(self, code):
        """ sends a command to the launcher """
        self.launcher.ctrl_transfer(0x21,0x09,0,0,code)

    def pan_left(self):
        """ pans launcher left """
        self.send(CODE_LEFT)

    def pan_right(self):
        """ pans launcher right """
        self.send(CODE_RIGHT)

    def tilt_up(self):
        """ tilts launcher up """
        self.send(CODE_UP)

    def tilt_down(self):
        """ tilts launcher down """
        self.send(CODE_DOWN)

    def stop(self):
        """ stops the current launcher action """
        self.send(CODE_STOP)

    def fire(self):
        """ fires a missile """
        self.send(CODE_FIRE)
