#include <sstream>
#include "ros/ros.h"
#include "OdomSource.h"

int main(int argc, char **argv)
{
  ros::init(argc,argv,"odomComb");
  ros::NodeHandle mNh;
  std::string odomPubName;
  mNh.param<std::string>("odomPub",odomPubName,"odomCombOut");
  ros::Publisher pub = mNh.advertise<nav_msgs::Odometry>(odomPubName,1,true);

  std::string paramBase = "~odomSource";
  std::vector<ros::NodeHandle> nodeHandles;
  std::vector<OdomSource> odomSources;

  int i = 0;
  std::stringstream st;
  st << paramBase << i;
  while(ros::param::has(st.str())) {
    ros::NodeHandle nh(st.str());
    std::cout << "Adding " << st.str() << std::endl;
    std::string topicName;
    nh.getParam("topic",topicName);
    double tConf, rConf; 
    nh.getParam("tConf",tConf);
    nh.getParam("rConf",rConf);
    nodeHandles.push_back(nh);
    odomSources.push_back(OdomSource(topicName,tConf,rConf));
    st.flush();
    st.seekp(0);
    st << paramBase << ++i;
  }
  std::cout << "Subscribing to topics" << std::endl;

  std::vector<ros::NodeHandle>::iterator nIt = nodeHandles.begin();
  for(std::vector<OdomSource>::iterator oIt = odomSources.begin();oIt < odomSources.end(); ++oIt)
  {
    const std::string topicName = oIt -> getName();
    nIt->subscribe(topicName,1,&OdomSource::odomCb,&*oIt);
    ++nIt;
  }
  ros::spin();
}
