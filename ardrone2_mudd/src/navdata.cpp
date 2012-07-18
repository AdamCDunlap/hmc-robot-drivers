#include <navdata.h>

int state = -1;
bool batWarn = false;

/* Initialization local variables before event loop  */
inline C_RESULT demo_navdata_client_init( void* data )
{
  return C_OK;
}

/* Receving navdata during the event loop */
inline C_RESULT demo_navdata_client_process( const navdata_unpacked_t* const navdata )
{
	const navdata_demo_t*nd = &navdata->navdata_demo;

  state = nd -> ctrl_state;

  if (state & ARDRONE_VBAT_LOW)
  {
    batWarn = true;
    printf("Low battery!\n");
  } else 
    batWarn = false;

  if(ros::ok()) {
      ardrone2_mudd::navData packet;

      packet.tag = nd -> tag;
      packet.size = nd -> size;
      packet.ctrlState = nd -> ctrl_state;
      packet.batLevel = nd -> vbat_flying_percentage;
      packet.theta = nd -> theta;
      packet.phi = nd -> phi;
      packet.psi = nd -> psi;
      packet.altitude = nd -> altitude;
      packet.vx = nd -> vx;
      packet.vy = nd -> vy;
      packet.vz = nd -> vz;
      packet.numFrames = nd -> num_frames;
      packet.wifiQuality = navdata->navdata_wifi.link_quality;

      navP.publish(packet);
      // Maybe this shouldnt be here?
      ros::spinOnce();
  }
  return C_OK;
}

/* Relinquish the local resources after the event loop exit */
inline C_RESULT demo_navdata_client_release( void )
{
  return C_OK;
}

/* Registering to navdata client */
BEGIN_NAVDATA_HANDLER_TABLE
  NAVDATA_HANDLER_TABLE_ENTRY(demo_navdata_client_init, demo_navdata_client_process, demo_navdata_client_release, NULL)
END_NAVDATA_HANDLER_TABLE

