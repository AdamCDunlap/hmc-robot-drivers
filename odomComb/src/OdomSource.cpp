#include "OdomSource.h"

OdomSource::OdomSource(std::string tName, double tC, double rC): topicName(tName), tConf(tC), rConf(rC), updated(false) 
{
}

void OdomSource::odomCb(const nav_msgs::Odometry::ConstPtr &msg)
{
  lastOdom = msg;
}

std::string OdomSource::getName() const
{
  return topicName;
}

double OdomSource::getrConf() const
{
  return tConf;
}
double OdomSource::gettConf() const
{
  return rConf;
}
bool OdomSource::hasUpdated() const
{
  return updated;
}

std::ostream& operator<<(std::ostream& out, const OdomSource& os)
{
  out << os.getName() << " " << os.getrConf() << " " << os.gettConf(); 
  return out;
}
