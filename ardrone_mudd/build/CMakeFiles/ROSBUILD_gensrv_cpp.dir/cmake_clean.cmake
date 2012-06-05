FILE(REMOVE_RECURSE
  "../msg_gen"
  "../srv_gen"
  "../src/ardrone_mudd/msg"
  "../src/ardrone_mudd/srv"
  "../msg_gen"
  "../srv_gen"
  "CMakeFiles/ROSBUILD_gensrv_cpp"
  "../srv_gen/cpp/include/ardrone_mudd/Control.h"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/ROSBUILD_gensrv_cpp.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
