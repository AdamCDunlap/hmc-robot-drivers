#include "ros/ros.h"
#include "ardrone_mudd/navData.h"
#include <Navdata/navdata.h>

extern "C" {
#include <ardrone_tool/Navdata/ardrone_navdata_client.h>
#include <stdio.h>
}

ros::NodeHandle *n;
ros::Publisher *navDataPub;
int state;

inline C_RESULT demo_navdata_client_init( void* data )
{
  char **argv;
  int argc = 0;
  int state = -1;
  ros::init(argc,argv, "navData");
  n = new ros::NodeHandle();
  navDataPub = new ros::Publisher( n->advertise<ardrone_mudd::navData>("navData",0) );
  return C_OK;
}

bool isEmer()
{
    if (state == 0)
        return true;
    return false;
}

/* Receving navdata during the event loop */
inline C_RESULT demo_navdata_client_process( const navdata_unpacked_t* const navdata )
{
	const navdata_demo_t*nd = &navdata->navdata_demo;

	//printf("=====================\nNavdata for flight demonstrations =====================\n\n");

	//printf("Control state : %i\n",nd->ctrl_state);
	//printf("Battery level : %i mV\n",nd->vbat_flying_percentage);
	//printf("Orientation   : [Theta] %4.3f  [Phi] %4.3f  [Psi] %4.3f\n",nd->theta,nd->phi,nd->psi);
	//printf("Altitude      : %i\n",nd->altitude);
	//printf("Speed         : [vX] %4.3f  [vY] %4.3f  [vZPsi] %4.3f\n",nd->theta,nd->phi,nd->psi);

	//printf("\033[1A");
    if(ros::ok())
    {
        //printf("Altitude      : %i\n",nd->altitude);
        //printf("Speed         : [vX] %4.3f  [vY] %4.3f  [vZPsi] %4.3f\n",nd->theta,nd->phi,nd->psi);

        //printf("\033[1A");
        ardrone_mudd::navData packet;

        state = nd -> ctrl_state;
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

        navDataPub->publish(packet);
        // Maybe this shouldnt be here?
        ros::spinOnce();
    }
  return C_OK;
}

inline C_RESULT demo_navdata_client_release( void )
{
    delete n;
    delete navDataPub;
  return C_OK;
}

BEGIN_NAVDATA_HANDLER_TABLE
  NAVDATA_HANDLER_TABLE_ENTRY(demo_navdata_client_init, demo_navdata_client_process, demo_navdata_client_release, NULL)
END_NAVDATA_HANDLER_TABLE
