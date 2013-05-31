#ifndef ODOM_SOURCE_H
#define ODOM_SOURCE_H

#include "ros/ros.h"
#include "ros/time.h"
#include "nav_msgs/Odometry.h"
#include <tf/transform_listener.h>
#include <tf/transform_broadcaster.h>
#include <iostream>
// #include <vector>

class OdomSource
{
public:
  OdomSource(std::string tName, double tConf, double rConf);
  //~OdomSource();
  std::string getName() const;
  double getrConf() const;
  double gettConf() const;
  std::vector<double> getdPos();
  tf::Quaternion getdQuat();
  void odomCb(const nav_msgs::Odometry::ConstPtr &msg);
  void resetPos();
  bool hasUpdated() const;
  bool hasNotUpdated() const;
private:
  std::string topicName;
  double tConf;
  double rConf;
  double dx;
  double dy;
  double dz;
  tf::Quaternion dQuat;
  nav_msgs::Odometry::ConstPtr lastOdom;
  bool updated;
};

std::ostream& operator<<(std::ostream& out, const OdomSource& os);

#endif // ODOM_SOURCE_H
