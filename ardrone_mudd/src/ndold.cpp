#include "ros/ros.h"
#include "ardrone_mudd3/navData.h"
#include "std_msgs/String.h"
#include <sstream>

int main(int argc, char **argv)
{
  ros::init(argc, argv, "navData");
  ros::NodeHandle n;

  ros::Publisher navDataPub = n.advertise<ardrone_mudd::navData>("navData",5);
  ros::Rate loop_rate(10);
  
  while (ros::ok())
  {
    ardrone_mudd::navData packet;
    packet.altitude = 40;
    navDataPub.publish(packet);
    ros::spinOnce();
    loop_rate.sleep();
  }

  return 0;
}
