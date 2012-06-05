FILE(REMOVE_RECURSE
  "../msg_gen"
  "../srv_gen"
  "../src/ardrone_mudd/msg"
  "../src/ardrone_mudd/srv"
  "../msg_gen"
  "../srv_gen"
  "CMakeFiles/ROSBUILD_genmsg_lisp"
  "../msg_gen/lisp/navData.lisp"
  "../msg_gen/lisp/_package.lisp"
  "../msg_gen/lisp/_package_navData.lisp"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/ROSBUILD_genmsg_lisp.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
