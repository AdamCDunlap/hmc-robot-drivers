#ifndef _CONFIG_H_
#define _CONFIG_H_

#include "ardrone2_mudd/Config.h"
//#include "driver.h"

extern "C" {
#include "ardrone_tool/UI/ardrone_input.h"
#include "ardrone_tool/ardrone_tool_configuration.h"
}

#include "ros/ros.h"

bool configCb(ardrone2_mudd::Config::Request &req, 
               ardrone2_mudd::Config::Response &res);

#endif // _CONFIG_H_
