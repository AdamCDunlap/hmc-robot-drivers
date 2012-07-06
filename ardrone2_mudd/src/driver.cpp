#include <driver.h>

#include <cv_bridge/CvBridge.h>
static uint8_t*  pixbuf_data       = NULL;
C_RESULT output_ros_stage_open( void *cfg, vp_api_io_data_t *in, vp_api_io_data_t *out)
{
  printf(">>>>>>>>>>>>>>>>>>>>>>> OPEN\n");
  return (SUCCESS);
}

C_RESULT output_ros_stage_transform( void *cfg, vp_api_io_data_t *in, vp_api_io_data_t *out)
{
  /* Get a reference to the last decoded picture */
  pixbuf_data      = (uint8_t*)in->buffers[0];

  
  IplImage *frame;
  frame=cvCreateImage(cvSize(320,240), IPL_DEPTH_8U, 3);
  frame->imageData = (char *)pixbuf_data;
  cvCvtColor(frame,frame,CV_BGR2RGB);
  

  sensor_msgs::ImagePtr msg = sensor_msgs::CvBridge::cvToImgMsg(frame,"bgr8");

  printf(">>>>>>>>>>> trans\n");
  printf("%i\n",pixbuf_data[0]);

  imageP.publish(msg);

  return (SUCCESS);
}

C_RESULT output_ros_stage_close( void *cfg, vp_api_io_data_t *in, vp_api_io_data_t *out)
{
  printf(">>>>>>>>>>>>>>> close\n");
  return (SUCCESS);
}


const vp_api_stage_funcs_t vp_stages_output_ros_funcs =
{
  NULL,
  (vp_api_stage_open_t)output_ros_stage_open,
  (vp_api_stage_transform_t)output_ros_stage_transform,
  (vp_api_stage_close_t)output_ros_stage_close
};

static int32_t exit_ihm_program = 1;
ros::Publisher navP;
image_transport::Publisher imageP;

/* Implementing Custom methods for the main function of an ARDrone application */
int main()
{
  char* s = "hellothere";
  int x = 1;
  ros::init(x,&s,"ardrone2");
  ros::NodeHandle nh("~");
  image_transport::ImageTransport ith(nh);
  navP = nh.advertise<ardrone2_mudd::navData>("navData",1);
  ros::ServiceServer controlSrv = nh.advertiseService("heli",controlCb);
  imageP = ith.advertise("camera/image",1);
	return ardrone_tool_main(1, &s);
}

/* The delegate object calls this method during initialization of an ARDrone application */
C_RESULT ardrone_tool_init_custom(void)
{
  /* Registering for a new device of game controller */
   ardrone_tool_input_add( &rosControl );

   ardrone_application_default_config.navdata_options = NAVDATA_OPTION_FULL_MASK; 
   ardrone_application_default_config.video_codec = UVLC_CODEC;
   ardrone_application_default_config.bitrate_ctrl_mode = 1;

    /************************ VIDEO STAGE CONFIG ******************************/
    #define ROS_POST_STAGES   2
    uint8_t post_stages_index = 0;

    //Alloc structs
    specific_parameters_t * params             = (specific_parameters_t *)vp_os_calloc(1,sizeof(specific_parameters_t));
    specific_stages_t * ros_pre_stages  = (specific_stages_t*)vp_os_calloc(1, sizeof(specific_stages_t));
    specific_stages_t * ros_post_stages = (specific_stages_t*)vp_os_calloc(1, sizeof(specific_stages_t));
    vp_api_picture_t  * in_picture             = (vp_api_picture_t*) vp_os_calloc(1, sizeof(vp_api_picture_t));
    vp_api_picture_t  * out_picture            = (vp_api_picture_t*) vp_os_calloc(1, sizeof(vp_api_picture_t));

    in_picture->width          = QVGA_WIDTH;
    in_picture->height         = QVGA_HEIGHT;

    out_picture->framerate     = 20;
    out_picture->format        = PIX_FMT_RGB24;
    out_picture->width         = QVGA_WIDTH;
    out_picture->height        = QVGA_HEIGHT;

    out_picture->y_buf         = (uint8_t*)vp_os_malloc( QVGA_WIDTH * QVGA_HEIGHT * 3 );
    out_picture->cr_buf        = NULL;
    out_picture->cb_buf        = NULL;

    out_picture->y_line_size   = QVGA_WIDTH * 3;
    out_picture->cb_line_size  = 0;
    out_picture->cr_line_size  = 0;

    //Alloc the lists
    ros_pre_stages->stages_list  = NULL;
    ros_post_stages->stages_list = (vp_api_io_stage_t*)vp_os_calloc(ROS_POST_STAGES,sizeof(vp_api_io_stage_t));
   
    ros_post_stages->stages_list[post_stages_index].name    = "ROS OUTPUT";
    ros_post_stages->stages_list[post_stages_index].type    = VP_API_OUTPUT_SDL;
    ros_post_stages->stages_list[post_stages_index].cfg     = NULL;
    ros_post_stages->stages_list[post_stages_index++].funcs   = vp_stages_output_ros_funcs;

    //Define the list of stages size
    ros_pre_stages->length  = 0;
    ros_post_stages->length = post_stages_index;

    params->in_pic = in_picture;
    params->out_pic = out_picture;
    params->pre_processing_stages_list  = ros_pre_stages;
    params->post_processing_stages_list = ros_post_stages;
    params->needSetPriority = 0;
    params->priority = 0;

    START_THREAD(video_stage, params);
    video_stage_init();
    //if (2 <= ARDRONE_VERSION ())
    //  {
    //    START_THREAD (video_recorder, NULL);
    //    video_recorder_init ();
    //  }
    //else
    //  {
    //    printf ("Don't start ... version is %d\n", ARDRONE_VERSION ());
    //  }


    video_stage_resume_thread();
   /* Start all threads of your application */
   //START_THREAD( video_stage, NULL );
  
  return C_OK;
}

/* The delegate object calls this method when the event loop exit */
C_RESULT ardrone_tool_shutdown_custom(void)
{
  /* Relinquish all threads of your application */
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

/* Implementing thread table in which you add routines of your application and those provided by the SDK */
BEGIN_THREAD_TABLE
  THREAD_TABLE_ENTRY( ardrone_control, 20 )
  THREAD_TABLE_ENTRY( navdata_update, 20 )
  THREAD_TABLE_ENTRY( video_stage, 20 )
END_THREAD_TABLE
