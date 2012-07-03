#include <driver.h>

static int32_t exit_ihm_program = 1;
ros::Publisher navP;

/* Implementing Custom methods for the main function of an ARDrone application */
int main()
{
  char* s = "hello";
  int x = 1;
  ros::init(x,&s,"ardrone2");
  ros::NodeHandle nh("~");
  navP = nh.advertise<ardrone2_mudd::navData>("navData",1);
  ros::ServiceServer controlSrv = nh.advertiseService("heli",controlCb);
	return ardrone_tool_main(1, &s);
}

/* The delegate object calls this method during initialization of an ARDrone application */
C_RESULT ardrone_tool_init_custom(void)
{
  /* Registering for a new device of game controller */
  // ardrone_tool_input_add( &gamepad );

  /* Start all threads of your application */
  START_THREAD( video_stage, NULL );
  
  return C_OK;
}

/* The delegate object calls this method when the event loop exit */
C_RESULT ardrone_tool_shutdown_custom(void)
{
  /* Relinquish all threads of your application */
  JOIN_THREAD( video_stage );

  /* Unregistering for the current device */
  // ardrone_tool_input_remove( &gamepad );

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

/* Implementing thread table in which you add routines of your application and those provided by the SDK */
BEGIN_THREAD_TABLE
  THREAD_TABLE_ENTRY( ardrone_control, 20 )
  THREAD_TABLE_ENTRY( navdata_update, 20 )
//  THREAD_TABLE_ENTRY( video_stage, 20 )
END_THREAD_TABLE
