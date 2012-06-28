#ifndef ODOM_SOURCE_H
#define ODOM_SOURCE_H

#include "ros/ros.h"
#include "ros/time.h"
#include "nav_msgs/Odometry.h"
#include <iostream>

class OdomSource
{
public:
  OdomSource(std::string tName, double tConf, double rConf);
  //~OdomSource();
  std::string getName() const;
  double getrConf() const;
  double gettConf() const;
  void odomCb(const nav_msgs::Odometry::ConstPtr &msg);
  bool hasUpdated() const;
private:
  std::string topicName;
  double tConf;
  double rConf;
  nav_msgs::Odometry::ConstPtr lastOdom;
  bool updated;
};

std::ostream& operator<<(std::ostream& out, const OdomSource& os);

#endif // ODOM_SOURCE_H
