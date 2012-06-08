#include "ros/ros.h"
#include "Control/control.h"

#include <string>
#include <sstream>
#include <algorithm>
#include <iostream>
#include <iterator>

int takeoff = 0;
int camera = 0;
bool hasReset = false;
bool reset = false;
bool configChange = false;
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
    if(reset)
    {
        reset = false;
        takeoff = 0;
        printf("resetting\n");
        ardrone_tool_set_ui_pad_select(0);
        ardrone_tool_set_ui_pad_select(1);
    }

    if(configChange)
    {
        printf("Config change\n");
        ARDRONE_TOOL_CONFIGURATION_ADDEVENT(video_channel,&camera,NULL);
        //ardrone_tool_configuration_event_configure();
        configChange = false;
    }
    ardrone_tool_set_ui_pad_start(takeoff);
    if (takeoff == 1)
        ardrone_at_set_progress_cmd(flag,phi,theta,gaz,yaw);
    return C_OK;
}

C_RESULT controlEnd( void )
{
  return C_OK;
}

bool controlCb(ardrone_mudd::Control::Request &req, 
               ardrone_mudd::Control::Response &res)
{
    using namespace std;
    vector<string> command;
    istringstream iss(req.command);
    copy(istream_iterator<string>(iss),
            istream_iterator<string>(),
            back_inserter<vector<string> >(command));


    cout << "Command: " << req.command << endl;
    res.result = false;  
    if (command[0].compare("takeoff") == 0)
    {
        printf("taking off\n");
        takeoff = 1;

        flag = 0; 
        phi = 0; 
        theta = 0;
        gaz = 0; 
        yaw = 0;

        res.result = true;
    } else if (command[0].compare("land") == 0) {
        takeoff = 0;
        printf("landing\n");
        res.result = true;
    } else if (command[0].compare("reset") == 0) {
        printf("trying to reset\n");
        reset = true;
        res.result = true;
    } else if (command[0].compare("camera") == 0) {
        int channel = atoi(command[1].c_str());
        printf("changing camera\n");
        if((channel < 4) && (channel > -1))
        {
            configChange = true;
            res.result = true;
            camera = channel;
        }
        else
            res.result = false;
    } else if (command[0].compare("heli") == 0) {
        int Tflag    = atoi(command[1].c_str());
        float Tphi   = atof(command[2].c_str());
        float Ttheta = atof(command[3].c_str());
        float Tgaz   = atof(command[4].c_str());
        float Tyaw   = atof(command[5].c_str());

        printf("heli\n");
        if (!( (Tflag == 0) || (Tflag == 1)) )
            res.result = false;
        else if ((Tflag > 1) || (Tflag < -1))
            res.result = false;
        else if ((Tphi > 1) || (Tphi < -1))
            res.result = false;
        else if ((Ttheta > 1) || (Ttheta < -1))
            res.result = false;
        else if ((Tgaz > 1) || (Tgaz < -1))
            res.result = false;
        else if ((Tyaw > 1) || (Tyaw < -1))
            res.result = false;
        else
        {
            flag   = Tflag;
            phi    = Tphi;
            theta  = Ttheta;
            gaz    = Tgaz;
            yaw    = Tyaw; 
            res.result = true;
        }
        if (!res.result)
        {
            printf("Invalid arguments\n");
            printf("Flag must be 0 or 1\n");
            printf("phi,theta,gaz,yaw must be between -1 and 1\n");
        }
    } else {
        cout << "unknown command: " << req.command << endl;
        res.result = false;
    }
  return true;
}


input_device_t rosControl = {
    "rosControl",
    controlStart,
    controlSend,
    controlEnd
};
