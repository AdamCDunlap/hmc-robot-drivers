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
link_directories(${PROJECT_SOURCE_DIR}/lib)
#rosbuild_add_boost_directories()
#rosbuild_link_boost(${PROJECT_NAME} thread)
set(SDKPATH src/ARDroneLib)
include_directories(${SDKPATH} ${SDKPATH}/VP_SDK ${SDKPATH}/Soft/Lib ${SDKPATH}/VP_SDK/VP_Os/linux ${SDKPATH}/Soft/Common src/)
rosbuild_add_executable(driver src/driver.cpp src/Navdata/navdata.cpp src/Video/video_stage.cpp src/Control/control.cpp)
rosbuild_add_executable(imageViewer nodes/image.cpp)
target_link_libraries(driver libpc_ardrone.a libvlib.a libsdk.a SDL)
