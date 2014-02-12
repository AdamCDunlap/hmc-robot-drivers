/* Auto-generated by genmsg_cpp for file /home/robotics/rosbots/neato_mudd/msg/HallwayType.msg */
#ifndef NEATO_MUDD_MESSAGE_HALLWAYTYPE_H
#define NEATO_MUDD_MESSAGE_HALLWAYTYPE_H
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

namespace neato_mudd
{
template <class ContainerAllocator>
struct HallwayType_ {
  typedef HallwayType_<ContainerAllocator> Type;

  HallwayType_()
  : header()
  , hall_type()
  {
  }

  HallwayType_(const ContainerAllocator& _alloc)
  : header(_alloc)
  , hall_type(_alloc)
  {
  }

  typedef  ::std_msgs::Header_<ContainerAllocator>  _header_type;
   ::std_msgs::Header_<ContainerAllocator>  header;

  typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _hall_type_type;
  std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  hall_type;


  typedef boost::shared_ptr< ::neato_mudd::HallwayType_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::neato_mudd::HallwayType_<ContainerAllocator>  const> ConstPtr;
  boost::shared_ptr<std::map<std::string, std::string> > __connection_header;
}; // struct HallwayType
typedef  ::neato_mudd::HallwayType_<std::allocator<void> > HallwayType;

typedef boost::shared_ptr< ::neato_mudd::HallwayType> HallwayTypePtr;
typedef boost::shared_ptr< ::neato_mudd::HallwayType const> HallwayTypeConstPtr;


template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const  ::neato_mudd::HallwayType_<ContainerAllocator> & v)
{
  ros::message_operations::Printer< ::neato_mudd::HallwayType_<ContainerAllocator> >::stream(s, "", v);
  return s;}

} // namespace neato_mudd

namespace ros
{
namespace message_traits
{
template<class ContainerAllocator> struct IsMessage< ::neato_mudd::HallwayType_<ContainerAllocator> > : public TrueType {};
template<class ContainerAllocator> struct IsMessage< ::neato_mudd::HallwayType_<ContainerAllocator>  const> : public TrueType {};
template<class ContainerAllocator>
struct MD5Sum< ::neato_mudd::HallwayType_<ContainerAllocator> > {
  static const char* value() 
  {
    return "a376eedad63156218bfb104e43549ded";
  }

  static const char* value(const  ::neato_mudd::HallwayType_<ContainerAllocator> &) { return value(); } 
  static const uint64_t static_value1 = 0xa376eedad6315621ULL;
  static const uint64_t static_value2 = 0x8bfb104e43549dedULL;
};

template<class ContainerAllocator>
struct DataType< ::neato_mudd::HallwayType_<ContainerAllocator> > {
  static const char* value() 
  {
    return "neato_mudd/HallwayType";
  }

  static const char* value(const  ::neato_mudd::HallwayType_<ContainerAllocator> &) { return value(); } 
};

template<class ContainerAllocator>
struct Definition< ::neato_mudd::HallwayType_<ContainerAllocator> > {
  static const char* value() 
  {
    return "Header header\n\
string hall_type\n\
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

  static const char* value(const  ::neato_mudd::HallwayType_<ContainerAllocator> &) { return value(); } 
};

template<class ContainerAllocator> struct HasHeader< ::neato_mudd::HallwayType_<ContainerAllocator> > : public TrueType {};
template<class ContainerAllocator> struct HasHeader< const ::neato_mudd::HallwayType_<ContainerAllocator> > : public TrueType {};
} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

template<class ContainerAllocator> struct Serializer< ::neato_mudd::HallwayType_<ContainerAllocator> >
{
  template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
  {
    stream.next(m.header);
    stream.next(m.hall_type);
  }

  ROS_DECLARE_ALLINONE_SERIALIZER;
}; // struct HallwayType_
} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::neato_mudd::HallwayType_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const  ::neato_mudd::HallwayType_<ContainerAllocator> & v) 
  {
    s << indent << "header: ";
s << std::endl;
    Printer< ::std_msgs::Header_<ContainerAllocator> >::stream(s, indent + "  ", v.header);
    s << indent << "hall_type: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.hall_type);
  }
};


} // namespace message_operations
} // namespace ros

#endif // NEATO_MUDD_MESSAGE_HALLWAYTYPE_H

