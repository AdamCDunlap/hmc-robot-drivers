FILE(REMOVE_RECURSE
  "../msg_gen"
  "../srv_gen"
  "../src/ardrone2_mudd/msg"
  "../src/ardrone2_mudd/srv"
  "../msg_gen"
  "../srv_gen"
  "CMakeFiles/ROSBUILD_gensrv_lisp"
  "../srv_gen/lisp/Config.lisp"
  "../srv_gen/lisp/_package.lisp"
  "../srv_gen/lisp/_package_Config.lisp"
  "../srv_gen/lisp/Control.lisp"
  "../srv_gen/lisp/_package.lisp"
  "../srv_gen/lisp/_package_Control.lisp"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/ROSBUILD_gensrv_lisp.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
