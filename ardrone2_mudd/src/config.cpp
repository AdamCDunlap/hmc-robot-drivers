#include "config.h"

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

