#include "config.hpp"

#include <string>
#include <sstream>
#include <algorithm>
#include <iostream>
#include <iterator>

//C_RESULT configStart( void )
//{
//  return C_OK;
//}
//
//C_RESULT configSend( void )
//{
//  return C_OK;
//}
//
//C_RESULT configEnd( void )
//{
//  return C_OK;
//}

bool configCb(ardrone2_mudd::Config::Request &req, 
               ardrone2_mudd::Config::Response &res)
{
  std::vector<std::string> command;
  std::istringstream iss(req.command);
  std::copy(std::istream_iterator<std::string>(iss),
       std::istream_iterator<std::string>(),
       std::back_inserter<std::vector<std::string> >(command));

  //printf("Command: %s", req.command);
  if (command[0].compare("camera"))
  {
    int channel = atoi(command[1].c_str());
    if ((channel >= 1) && (channel <= 4))
      ardrone_application_default_config.video_channel = channel;
  }
  
  return true;
}

