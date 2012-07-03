#include "ros/ros.h"
#include "Control/control.h"

#include <string>
#include <sstream>
#include <algorithm>
#include <iostream>
#include <iterator>

int takeoff = 0;
int flag = 0; // 0 hover , 1 otherwise?
float phi = 0; // -1 < left right angle  < 1
float theta = 0; //    front back angle
float gaz = 0; //      vertical speed
float yaw = 0; //      angular speed


C_RESULT controlStart( void )
{
  return C_OK;
}

C_RESULT controlSend( void )
{
    //if(reset)
    //{
    //    reset = false;
    //    takeoff = 0;
    //    printf("resetting\n");
    //    ardrone_tool_set_ui_pad_select(0);
    //    ardrone_tool_set_ui_pad_select(1);
    //    emerNum = 0;
    //}
    //else 
    //{
    //    if (emerNum % 100 == 0)
    //        printf("Emergency detected\n");
    //    takeoff = 0;
    //    ++emerNum;
    //}
   

    //if(configChange)
    //{
    //    printf("Config change\n");
    //    ARDRONE_TOOL_CONFIGURATION_ADDEVENT(video_channel,&camera,NULL);
    //    //ardrone_tool_configuration_event_configure();
    //    configChange = false;
    //}
    //if(retrim)
    //{
    //    retrim = false;
    //    printf("Resetting trim\n");
    //    ardrone_at_set_flat_trim();
    //}
    ardrone_tool_set_ui_pad_start(takeoff);
    if(takeoff)
      ardrone_tool_set_progressive_cmd(flag,phi,theta,gaz,yaw,0,0);
    return C_OK;
}

C_RESULT controlEnd( void )
{
  return C_OK;
}

bool controlCb(ardrone2_mudd::Control::Request &req, 
               ardrone2_mudd::Control::Response &res)
{
    if (req.flag == 2)
    {
        takeoff = 0;
        flag = 0; 
        phi = 0; 
        theta = 0;
        gaz = 0; 
        yaw = 0;
        printf("landing\n");
    } else if (req.flag == 3) {
        takeoff = 1;
        flag = 0; 
        phi = 0; 
        theta = 0;
        gaz = 0; 
        yaw = 0;
        printf("takeoff\n");
    } else if (req.flag == 4) {
        printf("trying to reset\n");
    } else if ( ( req.flag==1) || ( req.flag==0) ) {
      bool result = true; 
      if ((req.roll > 1) || (req.roll < -1))
        result = false;
      else if ((req.pitch > 1) || (req.pitch < -1))
        result = false;
      else if ((req.gaz > 1) || (req.gaz < -1))
        result = false;
      else if ((req.yaw > 1) || (req.yaw < -1))
        result = false;
      else
      {
        flag   = req.flag;
        phi    = req.roll;
        theta  = req.pitch;
        gaz    = req.gaz;
        yaw    = req.yaw; 
      }
      if (!result)
      {
        printf("Invalid arguments\n");
        printf("Flag must be 0 or 1\n");
        printf("phi,theta,gaz,yaw must be between -1 and 1\n");
      }
    } else {
      printf("Unknown command: %i %1.3f %1.3f %1.3f %1.3f", req.flag,req.roll,req.pitch,req.gaz,req.yaw);
    }
  return true;
}


input_device_t rosControl = {
    "rosControl",
    controlStart,
    controlSend,
    controlEnd
};
