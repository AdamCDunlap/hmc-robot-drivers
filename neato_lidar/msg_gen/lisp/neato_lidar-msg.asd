
(cl:in-package :asdf)

(defsystem "neato_lidar-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "LidarRanges" :depends-on ("_package_LidarRanges"))
    (:file "_package_LidarRanges" :depends-on ("_package"))
    (:file "LidarRangesStrengths" :depends-on ("_package_LidarRangesStrengths"))
    (:file "_package_LidarRangesStrengths" :depends-on ("_package"))
  ))