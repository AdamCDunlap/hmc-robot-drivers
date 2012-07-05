cmake_minimum_required(VERSION 2.4.6)
include($ENV{ROS_ROOT}/core/rosbuild/rosbuild.cmake)

# Set the build type.  Options are:
#  Coverage       : w/ debug symbols, w/o optimization, w/ code-coverage
#  Debug          : w/ debug symbols, w/o optimization
#  Release        : w/o debug symbols, w/ optimization
#  RelWithDebInfo : w/ debug symbols, w/ optimization
#  MinSizeRel     : w/o debug symbols, w/ optimization, stripped binaries
#set(ROS_BUILD_TYPE RelWithDebInfo)

rosbuild_init()
#execute_process(COMMAND cmake -E chdir ${PROJECT_SOURCE_DIR} make -f Make.ardronelib)

#set the default path for built executables to the "bin" directory
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)
#set the default path for built libraries to the "lib" directory
set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/lib)

#uncomment if you have defined messages
rosbuild_genmsg()
#uncomment if you have defined services
rosbuild_gensrv()

#common commands for building c++ executables and libraries
#rosbuild_add_library(${PROJECT_NAME} src/example.cpp)
#target_link_libraries(${PROJECT_NAME} another_library)
#rosbuild_add_boost_directories()
#rosbuild_link_boost(${PROJECT_NAME} thread)
#rosbuild_add_executable(example examples/example.cpp)
#target_link_libraries(example ${PROJECT_NAME})

set(SDKPATH src/ARDroneLib)
include_directories(${SDKPATH} ${SDKPATH}/VP_SDK ${SDKPATH}/VP_SDK/VP_Os ${SDKPATH}/Soft/Lib ${SDKPATH}/VP_SDK/VP_Os/linux ${SDKPATH}/Soft/Common src/)
link_directories(${PROJECT_SOURCE_DIR}/lib)
rosbuild_add_executable(driver src/driver.cpp src/Navdata/navdata.cpp src/Video/video_stage.cpp src/Control/control.cpp)
add_definitions(-DUSE_LINUX=yes)
#rosbuild_add_executable(driver src/test.cpp)
#target_link_libraries(driver libpc_ardrone.a libvlib.a libswscale.a libavcodec.a libavutil.a libavdevice.a libavformat.a libavfilter.a libsdk.a libpc_ardrone.a SDL rt pthread)# libh264_dec_lib.a libbuf_api_lib.a)
target_link_libraries(driver libpc_ardrone.a gtk-x11-2.0 rt sdk swscale avformat avcodec avutil vlib pthread pc_ardrone gtk-x11-2.0 rt) 
