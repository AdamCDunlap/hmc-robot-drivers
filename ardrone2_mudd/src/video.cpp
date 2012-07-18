#include "video.h"

int stream_width;
int stream_height;
extern video_decoder_config_t vec;
//int ardrone2_width  = hdtv720P_WIDTH;
//int ardrone2_height = hdtv720P_HEIGHT;
static uint8_t*  pixbuf_data       = NULL;
C_RESULT output_ros_stage_open( void *cfg, vp_api_io_data_t *in, vp_api_io_data_t *out)
{
  return (SUCCESS);
}

C_RESULT output_ros_stage_transform( video_decoder_config_t *cfg, vp_api_io_data_t *in, vp_api_io_data_t *out)
{
  /* Get a reference to the last decoded picture */
  pixbuf_data      = (uint8_t*)in->buffers[0];

  IplImage *frame;

  if(IS_ARDRONE2) {
    if( (currentCamera==0) || (currentCamera == 2) )
    {
      stream_width  = hdtv720P_WIDTH;
      stream_height = hdtv720P_HEIGHT;
    } else {
      stream_width  = hdtv360P_WIDTH;
      stream_height = hdtv360P_HEIGHT;
    }
  } else {
    if( (currentCamera==0) || (currentCamera == 2) )
    {
      stream_width  = QVGA_WIDTH;
      stream_height = QVGA_HEIGHT;
    } else {
      stream_width  = QCIF_WIDTH;
      stream_height = QCIF_HEIGHT;
    }
  }

  frame=cvCreateImage(cvSize(cfg->dst_picture->width,cfg->dst_picture->height), IPL_DEPTH_8U, 3);
  //frame=cvCreateImage(cvSize(stream_width,stream_height), IPL_DEPTH_8U, 3);
  frame->imageData = (char *)pixbuf_data;
  cvCvtColor(frame,frame,CV_BGR2RGB);
  

  //cv::Mat_<cv::Vec3b>& img = (cv::Mat_<cv::Vec3b>&)pixbuf_data;
  //cv::Mat_<cv::Vec3b>& img = (cv::Mat_<cv::Vec3b>&)in->buffers[0];
  //cv_bridge::CvImage cvimg;
  //cvimg.image = img;
  //cvimg.encoding = "bgr8";
  //cv::Mat img;
  //img.data = pixbuf_data;

  //cv_bridge::CvImage bimg;
  //bimg.image = img;
  //bimg.encoding ="bgr8";

  sensor_msgs::ImagePtr msg = sensor_msgs::CvBridge::cvToImgMsg(frame,"bgr8");
  if ((currentCamera == 0) || (currentCamera == 2))
    msg->header.frame_id = frontFrame;
  else
    msg->header.frame_id = downFrame;
  imageP.publish(msg);
  cvReleaseImage(&frame); 
  return (SUCCESS);
}

C_RESULT output_ros_stage_close( void *cfg, vp_api_io_data_t *in, vp_api_io_data_t *out)
{
  return (SUCCESS);
}


const vp_api_stage_funcs_t vp_stages_output_ros_funcs =
{
  NULL,
  (vp_api_stage_open_t)output_ros_stage_open,
  (vp_api_stage_transform_t)output_ros_stage_transform,
  (vp_api_stage_close_t)output_ros_stage_close
};

void videoInit()
{
    #define ROS_POST_STAGES   2
    uint8_t post_stages_index = 0;

    if (IS_ARDRONE2)
    {
      stream_width  = hdtv720P_WIDTH;
      stream_height  = hdtv720P_HEIGHT;
    } else {
      stream_width  = QVGA_WIDTH;
      stream_height = QVGA_HEIGHT;
    }

    specific_parameters_t * params             = (specific_parameters_t *)vp_os_calloc(1,sizeof(specific_parameters_t));
    specific_stages_t * ros_pre_stages  = (specific_stages_t*)vp_os_calloc(1, sizeof(specific_stages_t));
    specific_stages_t * ros_post_stages = (specific_stages_t*)vp_os_calloc(1, sizeof(specific_stages_t));
    vp_api_picture_t  * in_picture             = (vp_api_picture_t*) vp_os_calloc(1, sizeof(vp_api_picture_t));
    vp_api_picture_t  * out_picture            = (vp_api_picture_t*) vp_os_calloc(1, sizeof(vp_api_picture_t));

    in_picture->width          = stream_width;
    in_picture->height         = stream_height;

    out_picture->framerate     = 20;
    out_picture->format        = PIX_FMT_RGB24;
    out_picture->width         = stream_width;
    out_picture->height        = stream_height;

    out_picture->y_buf         = (uint8_t*)vp_os_malloc( stream_width * stream_height * 3 );
    out_picture->cr_buf        = NULL;
    out_picture->cb_buf        = NULL;

    out_picture->y_line_size   = stream_width * 3;
    out_picture->cb_line_size  = 0;
    out_picture->cr_line_size  = 0;

    //Alloc the lists
    ros_pre_stages->stages_list  = NULL;
    ros_post_stages->stages_list = (vp_api_io_stage_t*)vp_os_calloc(ROS_POST_STAGES,sizeof(vp_api_io_stage_t));
   
    ros_post_stages->stages_list[post_stages_index].name    = "ROS OUTPUT";
    ros_post_stages->stages_list[post_stages_index].type    = VP_API_OUTPUT_SDL;
    ros_post_stages->stages_list[post_stages_index].cfg     = (void *)&vec;
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
    video_stage_resume_thread();
}
