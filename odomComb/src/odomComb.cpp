#include <sstream>
#include "ros/ros.h"
#include "OdomSource.h"
#include <tf/transform_listener.h>
#include <tf/transform_broadcaster.h>
#include "std_msgs/String.h"

typedef std::vector<OdomSource>::iterator odomIter;

void sumPosVectors(std::vector<double> &result, std::vector<double> const &summand, double const &weight)
{
  for (int i=0; i != result.size(); ++i)
     result[i] += summand[i]*weight;
}

void combineAndPublish(std::vector<OdomSource> &odomSources, ros::Publisher &pub, double tTotal, double rTotal, std::vector<double>& resultPos, std::vector<double>& resultQuat)
{
  //For Now, just doing the simple way, a straightforward weighted average of the odometry sources. 

  for (odomIter oIt = odomSources.begin(); oIt != odomSources.end(); ++oIt)
  {
    std::cout << "Result x: " << resultPos[0] << " Current Odom: " <<  (oIt->getdPos())[0] << std::endl;
    std::cout << " conf: " << oIt->gettConf() << " weight: " << oIt->gettConf()/tTotal << std::endl;
    sumPosVectors(resultPos, oIt->getdPos(), oIt->gettConf()/tTotal);
    sumPosVectors(resultQuat, oIt->getdQuat(), oIt->getrConf()/rTotal);
    oIt->resetPos();
  }

  //Publishing the Message
  nav_msgs::Odometry odom_msg;
  odom_msg.header.stamp = ros::Time::now();
  odom_msg.header.frame_id = "odomCombOut";
  
  //Giving it the appropriate pose info
  odom_msg.pose.pose.position.x = resultPos[0];
  odom_msg.pose.pose.position.y = resultPos[1];
  odom_msg.pose.pose.position.z = resultPos[2];

  //constructing the quaternion
  //tf::Quaternion tf_odom_quat = tf::Quaternion(resultQuat[0], resultQuat[1], resultQuat[2], resultQuat[3]);
  //geometry_msgs::Quaternion odomQuat;
  //tf::quaternionTFToMsg(tf_odom_quat, odomQuat);
  //odom_msg.pose.pose.orientation = odomQuat;

  //Publish it
  pub.publish(odom_msg);
  
}

void odomCallBack(const nav_msgs::Odometry::ConstPtr &msg) 
{
  std::cout << "Recieving a callback" << std::endl;
}

int main(int argc, char **argv)
{
  ros::init(argc,argv,"odomComb");
  ros::NodeHandle mNh;
  std::string odomPubName;
  mNh.param<std::string>("odomPub",odomPubName,"odomCombOut");
  ros::Publisher pub = mNh.advertise<nav_msgs::Odometry>(odomPubName,1,true);

  std::string paramBase = "~odomSource";
  std::vector<ros::Subscriber> subscribers;
  std::vector<OdomSource> odomSources;

  int i = 0;
  std::stringstream st;
  st << paramBase << i;
  while(ros::param::has(st.str())) {
    ros::NodeHandle nh(st.str());
    std::cout << "Adding " << st.str();
    std::string topicName;
    nh.getParam("topic",topicName);
    std::cout << ", topic "<<topicName<<std::endl;
    double tConf, rConf; 
    nh.getParam("tConf",tConf);
    nh.getParam("rConf",rConf);
    odomSources.push_back(OdomSource(topicName,tConf,rConf));
    st.flush();
    st.seekp(0);
    st << paramBase << ++i;
  }
  std::cout << "Subscribing to topics" << std::endl;

  for(odomIter oIt = odomSources.begin(); oIt != odomSources.end(); ++oIt)
  {
    const std::string topicName = oIt -> getName();
    std::cout << "Subscribing to: "<< topicName << std::endl;
    subscribers.push_back(mNh.subscribe(topicName,1, &OdomSource::odomCb, &*oIt));
  }

  std::cout << "Subscribed to topics" << std::endl;
  
  double tTotal = 0;
  double rTotal = 0;
  for (odomIter oIt = odomSources.begin(); oIt != odomSources.end(); ++oIt)
  {
    tTotal += oIt->gettConf();
    rTotal += oIt->getrConf();
  }
  std::cout << "tTotal: " << tTotal << " rTotal: " << rTotal << std::endl;

  std::vector<double> resultPos;
  std::vector<double> resultQuat;
  for (int i = 0; i != 3; ++i)
  {
    resultQuat.push_back(0);
    resultPos.push_back(0);
  }
  resultQuat.push_back(0);

  while (true) {
    ros::spinOnce();
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
    {
      combineAndPublish(odomSources, pub, tTotal, rTotal, resultPos, resultQuat);
    }
  }
}
