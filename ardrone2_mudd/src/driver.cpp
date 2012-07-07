#include <driver.h>

static int32_t exit_ihm_program = 1;
ros::Publisher navP;
image_transport::Publisher imageP;
int currentCamera = 1;
std::string frontFrame = "front_camera";
std::string downFrame = "down_camera";

/* Implementing Custom methods for the main function of an ARDrone application */
int main()
{
  char* s = "hello";
  int x = 1;
  ros::init(x,&s,"ardrone2");
  ros::NodeHandle nh("~");
  image_transport::ImageTransport ith(nh);
  navP = nh.advertise<ardrone2_mudd::navData>("navData",1);
  ros::ServiceServer controlSrv = nh.advertiseService("heli",controlCb);
  ros::ServiceServer configSrv = nh.advertiseService("config",configCb);
  imageP = ith.advertise("camera/image",1);
	return ardrone_tool_main(1, &s);
}

/* The delegate object calls this method during initialization of an ARDrone application */
C_RESULT ardrone_tool_init_custom(void)
{
  /* Registering for a new device of game controller */
   ardrone_tool_input_add( &rosControl );

   ardrone_application_default_config.navdata_options = NAVDATA_OPTION_FULL_MASK; 

   ardrone_application_default_config.max_bitrate = 4000;
   ardrone_application_default_config.bitrate_ctrl_mode = VBC_MODE_DYNAMIC;

   if (IS_ARDRONE2)
     ardrone_application_default_config.video_codec = H264_720P_CODEC;
   else
   {
     ardrone_application_default_config.flying_mode = FLYING_MODE_HOVER_ON_TOP_OF_ORIENTED_ROUNDEL;
     ardrone_application_default_config.video_codec = UVLC_CODEC;
   }
   videoInit();

    //if (2 <= ARDRONE_VERSION ())
    //  {
    //    START_THREAD (video_recorder, NULL);
    //    video_recorder_init ();
    //  }
    //else
    //  {
    //    printf ("Don't start ... version is %d\n", ARDRONE_VERSION ());
    //  }
  return C_OK;
}

/* The delegate object calls this method when the event loop exit */
C_RESULT ardrone_tool_shutdown_custom(void)
{
  /* Relinquish all threads of your application */
  video_stage_resume_thread();
  JOIN_THREAD( video_stage );

  /* Unregistering for the current device */
   ardrone_tool_input_remove( &rosControl );

  return C_OK;
}

/* The event loop calls this method for the exit condition */
bool_t ardrone_tool_exit()
{
  return exit_ihm_program == 0;
}

C_RESULT signal_exit()
{
  exit_ihm_program = 0;

  return C_OK;
}

bool configCb(ardrone2_mudd::Config::Request &req, 
               ardrone2_mudd::Config::Response &res)
{
  std::vector<std::string> command;
  std::istringstream iss(req.command);
  std::copy(std::istream_iterator<std::string>(iss),
       std::istream_iterator<std::string>(),
       std::back_inserter<std::vector<std::string> >(command));

  printf("Command: %s \n", command[0].c_str());
  if (command[0].compare("camera") == 0) {
    int channel = atoi(command[1].c_str());
    if ((channel >= 0) && (channel <= 4))
    {
      if (channel == 4)
        currentCamera = (currentCamera + 1)%3;
      else
        currentCamera = channel;
      ARDRONE_TOOL_CONFIGURATION_ADDEVENT(video_channel, &channel, NULL);
    }
  } else if (command[0].compare("anim") == 0) {
    char buffer[128];
    int anim = atoi(command[1].c_str());
    snprintf(buffer,sizeof(buffer),"%i,%i",anim, MAYDAY_TIMEOUT[anim]);
    ARDRONE_TOOL_CONFIGURATION_ADDEVENT(flight_anim, buffer, NULL);
  } else if (command[0].compare("retrim") == 0) {
    ardrone_at_set_flat_trim();
  }
  
  return true;
}

/* Implementing thread table in which you add routines of your application and those provided by the SDK */
BEGIN_THREAD_TABLE
  THREAD_TABLE_ENTRY( ardrone_control, 20 )
  THREAD_TABLE_ENTRY( navdata_update, 20 )
  THREAD_TABLE_ENTRY( video_stage, 20 )
END_THREAD_TABLE
