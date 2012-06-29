#include "OdomSource.h"

OdomSource::OdomSource(std::string tName, double tC, double rC): topicName(tName), tConf(tC), rConf(rC), updated(false) 
{
}

void OdomSource::odomCb(const nav_msgs::Odometry::ConstPtr &msg)
{
  if (lastOdom)
  {
    dx += msg->pose.pose.position.x - lastOdom->pose.pose.position.x;
    dy += msg->pose.pose.position.y - lastOdom->pose.pose.position.y;
    dz += msg->pose.pose.position.z - lastOdom->pose.pose.position.z;
    dqx += msg->pose.pose.orientation.x - lastOdom->pose.pose.orientation.x;
    dqy += msg->pose.pose.orientation.y - lastOdom->pose.pose.orientation.y;
    dqz += msg->pose.pose.orientation.z - lastOdom->pose.pose.orientation.z;
    dqw += msg->pose.pose.orientation.w - lastOdom->pose.pose.orientation.w;
  }
  std::cout << topicName << ": " << dx << std::endl;
  lastOdom = msg;
  updated = true;
}

void OdomSource::resetPos()
{ 
  dx  = 0;
  dy  = 0;
  dz  = 0;
  dqx = 0;
  dqy = 0;
  dqz = 0;
  dqw = 0;
}

std::vector<double> OdomSource::getdPos()
{
  updated = false;
  std::vector<double> pos;
  std::cout<< "Dx: " << dx << std::endl;
  pos.push_back(dx);
  pos.push_back(dy);
  pos.push_back(dz);
  return pos;
}

std::vector<double> OdomSource::getdQuat()
{
  updated = false;
  std::vector<double> quat;
  quat.push_back(dqx);
  quat.push_back(dqy);
  quat.push_back(dqz);
  quat.push_back(dqw);
  return quat;
}

std::string OdomSource::getName() const
{
  return topicName;
}

double OdomSource::getrConf() const
{
  return rConf;
}
double OdomSource::gettConf() const
{
  return tConf;
}
bool OdomSource::hasUpdated() const
{
  return updated;
}

bool OdomSource::hasNotUpdated() const
{
  return !updated;
}

std::ostream& operator<<(std::ostream& out, const OdomSource& os)
{
  out << os.getName() << " " << os.getrConf() << " " << os.gettConf(); 
  return out;
}
