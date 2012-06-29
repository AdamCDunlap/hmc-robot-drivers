#include <sstream>
#include "ros/ros.h"
#include "OdomSource.h"

typedef std::vector<OdomSource>::iterator odomIter;

void sumPosVectors(std::vector<double> &result, std::vector<double> const &summand, double const &weight)
{
  for (int i=0; i != result.size(); ++i)
     result[i] += summand [i]*weight;
}

void combineAndPublish(std::vector<OdomSource> &odomSources, ros::Publisher &pub)
{
  //For Now, just doing the simple way, a straightforward weighted average of the odometry sources. 
  double tTotal = 0;
  double rTotal = 0;
  for (odomIter oIt = odomSources.begin(); oIt != odomSources.end(); ++oIt)
  {
    tTotal += oIt->gettConf();
    rTotal += oIt->getrConf();
  }
  std::vector<double> resultPos;
  resultPos.resize(3);
  std::vector<double> resultQuat;
  resultQuat.resize(4);
  for (int i = 0; i != 3; ++i)
  {
    resultQuat.push_back(0);
    resultPos.push_back(0);
  }
  resultQuat.push_back(0);

  for (odomIter oIt = odomSources.begin(); oIt != odomSources.end(); ++oIt)
  {
    sumPosVectors(resultPos, oIt->getdPos(), oIt->gettConf()/tTotal);
    sumPosVectors(resultQuat, oIt->getdQuat(), oIt->getrConf()/rTotal);
  }
}

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
  for(odomIter oIt = odomSources.begin(); oIt != odomSources.end(); ++oIt)
  {
    const std::string topicName = oIt -> getName();
    nIt->subscribe(topicName,1,&OdomSource::odomCb,&*oIt);
    ++nIt;
  }
  ros::spinOnce();
  while (true) {
    bool newPub = true;
    for (odomIter oIt = odomSources.begin(); oIt != odomSources.end(); ++oIt)
    {
      if (oIt -> hasNotUpdated())
      {
        newPub = false;
        break;
      }
    }
    if (newPub)
      combineAndPublish(odomSources, pub);
  }
}
