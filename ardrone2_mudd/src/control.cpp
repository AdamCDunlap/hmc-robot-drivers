#include "control.h"

int takeoff = 0;
int flag = 0; // 0 hover , 1 otherwise?
float phi = 0; // -1 < left right angle  < 1
float theta = 0; //    front back angle
float gaz = 0; //      vertical speed
float yaw = 0; //      angular speed
bool emerDetect = false;
bool reset = false;

C_RESULT controlStart( void )
{
  return C_OK;
}

C_RESULT controlSend( void )
{
  if(reset) {
    ardrone_tool_set_ui_pad_select(0);
    ardrone_tool_set_ui_pad_select(1);
    if (state != 0)
      reset = false;
  } else if (state & ARDRONE_EMERGENCY_MASK) { 
    if (!emerDetect) {
      printf("Emergency detected! \n");
      emerDetect = true;
    }
    takeoff = 0;
    flag = 0; // 0 hover , 1 otherwise?
    phi = 0; // -1 < left right angle  < 1
    theta = 0; //    front back angle
    gaz = 0; //      vertical speed
    yaw = 0; //      angular speed
  } else {
    emerDetect = false;
    //if(retrim)
    //{
    //    retrim = false;
    //    printf("Resetting trim\n");
    //    ardrone_at_set_flat_trim();
    //}
    ardrone_tool_set_ui_pad_start(takeoff);
    if(takeoff)
      ardrone_tool_set_progressive_cmd(flag,phi,theta,gaz,yaw,0,0);
  }
    return C_OK;
}

C_RESULT controlEnd( void )
{
  return C_OK;
}

bool controlCb(ardrone2_mudd::Control::Request &req, 
               ardrone2_mudd::Control::Response &res)
{
  if (req.flag == 2) {
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
    reset = true;
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

bool configCb(ardrone2_mudd::Config::Request &req, 
               ardrone2_mudd::Config::Response &res)
{
  std::vector<std::string> command;
  std::istringstream iss(req.command);
  std::copy(std::istream_iterator<std::string>(iss),
       std::istream_iterator<std::string>(),
       std::back_inserter<std::vector<std::string> >(command));

  printf("Command: %s \n", command[0].c_str());
  if (command[0].compare("camera") == 0) {
    int channel = atoi(command[1].c_str());
    if ((channel >= 0) && (channel <= 4))
    {
      if (channel == 4)
        currentCamera = (currentCamera + 1)%3;
      else
        currentCamera = channel;
      ARDRONE_TOOL_CONFIGURATION_ADDEVENT(video_channel, &channel, NULL);
    }
  } else if (command[0].compare("anim") == 0) {
    char buffer[128];
    int anim = atoi(command[1].c_str());
    snprintf(buffer,sizeof(buffer),"%i,%i",anim, MAYDAY_TIMEOUT[anim]);
    ARDRONE_TOOL_CONFIGURATION_ADDEVENT(flight_anim, buffer, NULL);
  } else if (command[0].compare("retrim") == 0) {
    ardrone_at_set_flat_trim();
  }
  
  return true;
}

