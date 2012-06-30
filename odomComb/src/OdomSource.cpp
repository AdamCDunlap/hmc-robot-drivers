#include "OdomSource.h"

OdomSource::OdomSource(std::string tName, double tC, double rC)
  : topicName(tName), tConf(tC), rConf(rC), dx(0), dy(0), dz(0),
    dQuat(tf::Quaternion::getIdentity()), lastOdom(), updated(false)
{

}

void OdomSource::odomCb(const nav_msgs::Odometry::ConstPtr &msg)
{
  double qx = msg->pose.pose.orientation.x;
  double qy = msg->pose.pose.orientation.y;
  double qz = msg->pose.pose.orientation.z;
  double qw = msg->pose.pose.orientation.w;
  tf::Quaternion newQuat = tf::Quaternion(qx,qy,qz,qw);
  tf::Quaternion oldQuatInv = tf::Quaternion::getIdentity();
  if (lastOdom)
  {
    dx += msg->pose.pose.position.x - lastOdom->pose.pose.position.x;
    dy += msg->pose.pose.position.y - lastOdom->pose.pose.position.y;
    dz += msg->pose.pose.position.z - lastOdom->pose.pose.position.z;
    double old_qx = lastOdom->pose.pose.orientation.x;
    double old_qy = lastOdom->pose.pose.orientation.y;
    double old_qz = lastOdom->pose.pose.orientation.z;
    double old_qw = lastOdom->pose.pose.orientation.w;
    oldQuatInv = tf::Quaternion(old_qx, old_qy, old_qz, old_qw).inverse();
  }
  else
  {
    dx = msg->pose.pose.position.x;
    dy = msg->pose.pose.position.y;
    dz = msg->pose.pose.position.z;
  }
  dQuat *= (oldQuatInv * newQuat);
  lastOdom = msg;
  updated = true;
}

void OdomSource::resetPos()
{ 
  dx  = 0;
  dy  = 0;
  dz  = 0;
  dQuat = tf::Quaternion::getIdentity();
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

tf::Quaternion OdomSource::getdQuat()
{
  updated = false;
  return dQuat;
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
