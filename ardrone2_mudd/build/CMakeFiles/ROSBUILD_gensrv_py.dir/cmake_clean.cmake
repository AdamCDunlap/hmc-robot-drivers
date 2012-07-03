FILE(REMOVE_RECURSE
  "../msg_gen"
  "../srv_gen"
  "../src/ardrone2_mudd/msg"
  "../src/ardrone2_mudd/srv"
  "../msg_gen"
  "../srv_gen"
  "CMakeFiles/ROSBUILD_gensrv_py"
  "../src/ardrone2_mudd/srv/__init__.py"
  "../src/ardrone2_mudd/srv/_Config.py"
  "../src/ardrone2_mudd/srv/_Control.py"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/ROSBUILD_gensrv_py.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
