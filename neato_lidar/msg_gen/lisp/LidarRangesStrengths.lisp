; Auto-generated. Do not edit!


(cl:in-package neato_lidar-msg)


;//! \htmlinclude LidarRangesStrengths.msg.html

(cl:defclass <LidarRangesStrengths> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (ranges
    :reader ranges
    :initarg :ranges
    :type (cl:vector cl:fixnum)
   :initform (cl:make-array 360 :element-type 'cl:fixnum :initial-element 0))
   (strengths
    :reader strengths
    :initarg :strengths
    :type (cl:vector cl:fixnum)
   :initform (cl:make-array 360 :element-type 'cl:fixnum :initial-element 0)))
)

(cl:defclass LidarRangesStrengths (<LidarRangesStrengths>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <LidarRangesStrengths>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'LidarRangesStrengths)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name neato_lidar-msg:<LidarRangesStrengths> is deprecated: use neato_lidar-msg:LidarRangesStrengths instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <LidarRangesStrengths>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader neato_lidar-msg:header-val is deprecated.  Use neato_lidar-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'ranges-val :lambda-list '(m))
(cl:defmethod ranges-val ((m <LidarRangesStrengths>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader neato_lidar-msg:ranges-val is deprecated.  Use neato_lidar-msg:ranges instead.")
  (ranges m))

(cl:ensure-generic-function 'strengths-val :lambda-list '(m))
(cl:defmethod strengths-val ((m <LidarRangesStrengths>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader neato_lidar-msg:strengths-val is deprecated.  Use neato_lidar-msg:strengths instead.")
  (strengths m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <LidarRangesStrengths>) ostream)
  "Serializes a message object of type '<LidarRangesStrengths>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:map cl:nil #'(cl:lambda (ele) (cl:write-byte (cl:ldb (cl:byte 8 0) ele) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) ele) ostream))
   (cl:slot-value msg 'ranges))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:write-byte (cl:ldb (cl:byte 8 0) ele) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) ele) ostream))
   (cl:slot-value msg 'strengths))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <LidarRangesStrengths>) istream)
  "Deserializes a message object of type '<LidarRangesStrengths>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
  (cl:setf (cl:slot-value msg 'ranges) (cl:make-array 360))
  (cl:let ((vals (cl:slot-value msg 'ranges)))
    (cl:dotimes (i 360)
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:aref vals i)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:aref vals i)) (cl:read-byte istream))))
  (cl:setf (cl:slot-value msg 'strengths) (cl:make-array 360))
  (cl:let ((vals (cl:slot-value msg 'strengths)))
    (cl:dotimes (i 360)
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:aref vals i)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:aref vals i)) (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<LidarRangesStrengths>)))
  "Returns string type for a message object of type '<LidarRangesStrengths>"
  "neato_lidar/LidarRangesStrengths")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'LidarRangesStrengths)))
  "Returns string type for a message object of type 'LidarRangesStrengths"
  "neato_lidar/LidarRangesStrengths")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<LidarRangesStrengths>)))
  "Returns md5sum for a message object of type '<LidarRangesStrengths>"
  "82e5c70e014b486ff6c31aa7c946a7cc")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'LidarRangesStrengths)))
  "Returns md5sum for a message object of type 'LidarRangesStrengths"
  "82e5c70e014b486ff6c31aa7c946a7cc")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<LidarRangesStrengths>)))
  "Returns full string definition for message of type '<LidarRangesStrengths>"
  (cl:format cl:nil "Header header~%uint16[360] ranges~%uint16[360] strengths~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.secs: seconds (stamp_secs) since epoch~%# * stamp.nsecs: nanoseconds since stamp_secs~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'LidarRangesStrengths)))
  "Returns full string definition for message of type 'LidarRangesStrengths"
  (cl:format cl:nil "Header header~%uint16[360] ranges~%uint16[360] strengths~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.secs: seconds (stamp_secs) since epoch~%# * stamp.nsecs: nanoseconds since stamp_secs~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <LidarRangesStrengths>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     0 (cl:reduce #'cl:+ (cl:slot-value msg 'ranges) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 2)))
     0 (cl:reduce #'cl:+ (cl:slot-value msg 'strengths) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 2)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <LidarRangesStrengths>))
  "Converts a ROS message object to a list"
  (cl:list 'LidarRangesStrengths
    (cl:cons ':header (header msg))
    (cl:cons ':ranges (ranges msg))
    (cl:cons ':strengths (strengths msg))
))
