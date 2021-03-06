/* Auto-generated by genmsg_cpp for file /home/luigi/ros_workspace/hmc-robot-drivers/neato_lidar/msg/LidarRanges.msg */
#ifndef NEATO_LIDAR_MESSAGE_LIDARRANGES_H
#define NEATO_LIDAR_MESSAGE_LIDARRANGES_H
#include <string>
#include <vector>
#include <map>
#include <ostream>
#include "ros/serialization.h"
#include "ros/builtin_message_traits.h"
#include "ros/message_operations.h"
#include "ros/time.h"

#include "ros/macros.h"

#include "ros/assert.h"

#include "std_msgs/Header.h"

namespace neato_lidar
{
template <class ContainerAllocator>
struct LidarRanges_ {
  typedef LidarRanges_<ContainerAllocator> Type;

  LidarRanges_()
  : header()
  , ranges()
  {
    ranges.assign(0);
  }

  LidarRanges_(const ContainerAllocator& _alloc)
  : header(_alloc)
  , ranges()
  {
    ranges.assign(0);
  }

  typedef  ::std_msgs::Header_<ContainerAllocator>  _header_type;
   ::std_msgs::Header_<ContainerAllocator>  header;

  typedef boost::array<uint16_t, 360>  _ranges_type;
  boost::array<uint16_t, 360>  ranges;


  typedef boost::shared_ptr< ::neato_lidar::LidarRanges_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::neato_lidar::LidarRanges_<ContainerAllocator>  const> ConstPtr;
  boost::shared_ptr<std::map<std::string, std::string> > __connection_header;
}; // struct LidarRanges
typedef  ::neato_lidar::LidarRanges_<std::allocator<void> > LidarRanges;

typedef boost::shared_ptr< ::neato_lidar::LidarRanges> LidarRangesPtr;
typedef boost::shared_ptr< ::neato_lidar::LidarRanges const> LidarRangesConstPtr;


template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const  ::neato_lidar::LidarRanges_<ContainerAllocator> & v)
{
  ros::message_operations::Printer< ::neato_lidar::LidarRanges_<ContainerAllocator> >::stream(s, "", v);
  return s;}

} // namespace neato_lidar

namespace ros
{
namespace message_traits
{
template<class ContainerAllocator> struct IsMessage< ::neato_lidar::LidarRanges_<ContainerAllocator> > : public TrueType {};
template<class ContainerAllocator> struct IsMessage< ::neato_lidar::LidarRanges_<ContainerAllocator>  const> : public TrueType {};
template<class ContainerAllocator>
struct MD5Sum< ::neato_lidar::LidarRanges_<ContainerAllocator> > {
  static const char* value() 
  {
    return "3f2297c661fa4a3bd816ee5dc6e68250";
  }

  static const char* value(const  ::neato_lidar::LidarRanges_<ContainerAllocator> &) { return value(); } 
  static const uint64_t static_value1 = 0x3f2297c661fa4a3bULL;
  static const uint64_t static_value2 = 0xd816ee5dc6e68250ULL;
};

template<class ContainerAllocator>
struct DataType< ::neato_lidar::LidarRanges_<ContainerAllocator> > {
  static const char* value() 
  {
    return "neato_lidar/LidarRanges";
  }

  static const char* value(const  ::neato_lidar::LidarRanges_<ContainerAllocator> &) { return value(); } 
};

template<class ContainerAllocator>
struct Definition< ::neato_lidar::LidarRanges_<ContainerAllocator> > {
  static const char* value() 
  {
    return "Header header\n\
uint16[360] ranges\n\
\n\
================================================================================\n\
MSG: std_msgs/Header\n\
# Standard metadata for higher-level stamped data types.\n\
# This is generally used to communicate timestamped data \n\
# in a particular coordinate frame.\n\
# \n\
# sequence ID: consecutively increasing ID \n\
uint32 seq\n\
#Two-integer timestamp that is expressed as:\n\
# * stamp.secs: seconds (stamp_secs) since epoch\n\
# * stamp.nsecs: nanoseconds since stamp_secs\n\
# time-handling sugar is provided by the client library\n\
time stamp\n\
#Frame this data is associated with\n\
# 0: no frame\n\
# 1: global frame\n\
string frame_id\n\
\n\
";
  }

  static const char* value(const  ::neato_lidar::LidarRanges_<ContainerAllocator> &) { return value(); } 
};

template<class ContainerAllocator> struct HasHeader< ::neato_lidar::LidarRanges_<ContainerAllocator> > : public TrueType {};
template<class ContainerAllocator> struct HasHeader< const ::neato_lidar::LidarRanges_<ContainerAllocator> > : public TrueType {};
} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

template<class ContainerAllocator> struct Serializer< ::neato_lidar::LidarRanges_<ContainerAllocator> >
{
  template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
  {
    stream.next(m.header);
    stream.next(m.ranges);
  }

  ROS_DECLARE_ALLINONE_SERIALIZER;
}; // struct LidarRanges_
} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::neato_lidar::LidarRanges_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const  ::neato_lidar::LidarRanges_<ContainerAllocator> & v) 
  {
    s << indent << "header: ";
s << std::endl;
    Printer< ::std_msgs::Header_<ContainerAllocator> >::stream(s, indent + "  ", v.header);
    s << indent << "ranges[]" << std::endl;
    for (size_t i = 0; i < v.ranges.size(); ++i)
    {
      s << indent << "  ranges[" << i << "]: ";
      Printer<uint16_t>::stream(s, indent + "  ", v.ranges[i]);
    }
  }
};


} // namespace message_operations
} // namespace ros

#endif // NEATO_LIDAR_MESSAGE_LIDARRANGES_H

