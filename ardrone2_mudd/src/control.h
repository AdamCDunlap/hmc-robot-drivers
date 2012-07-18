#ifndef _CONTROL_H_
#define _CONTROL_H_

#include <ros/ros.h>
#include <ardrone2_mudd/Control.h>
#include <ardrone2_mudd/Config.h>

extern "C" {
#include "ardrone_tool/UI/ardrone_input.h"
#include "ardrone_tool/ardrone_tool_configuration.h"
#include <config.h>
}

#include <string>
#include <sstream>
#include <algorithm>
#include <iostream>
#include <iterator>

#include "navdata.h"

extern input_device_t rosControl;
extern int camera;
bool controlCb(ardrone2_mudd::Control::Request &req, 
               ardrone2_mudd::Control::Response &res);
bool configCb(ardrone2_mudd::Config::Request &req, 
               ardrone2_mudd::Config::Response &res);

#endif // _CONTROL_H_
