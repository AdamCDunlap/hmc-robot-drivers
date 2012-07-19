#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <VP_Api/vp_api_stage.h>

extern ros::Publisher navP;
extern image_transport::Publisher imageP;
extern int currentCamera;
extern std::string frontFrame;
extern std::string downFrame;

extern const vp_api_stage_funcs_t vp_stages_output_ros_funcs;
extern void videoInit();
