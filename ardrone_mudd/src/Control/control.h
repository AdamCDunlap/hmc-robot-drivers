#ifndef _CONTROL_H_
#define _CONTROL_H_

#include "ardrone_mudd/Control.h"

extern "C" {
#include "ardrone_tool/UI/ardrone_input.h"
#include "ardrone_tool/ardrone_tool_configuration.h"
}

#include "Navdata/navdata.h"

extern input_device_t rosControl;
bool controlCb(ardrone_mudd::Control::Request &req, 
               ardrone_mudd::Control::Response &res);

#endif // _CONTROL_H_
