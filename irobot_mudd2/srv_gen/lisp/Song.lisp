; Auto-generated. Do not edit!


(cl:in-package irobot_mudd-srv)


;//! \htmlinclude Song-request.msg.html

(cl:defclass <Song-request> (roslisp-msg-protocol:ros-message)
  ((notes
    :reader notes
    :initarg :notes
    :type (cl:vector cl:fixnum)
   :initform (cl:make-array 0 :element-type 'cl:fixnum :initial-element 0))
   (durations
    :reader durations
    :initarg :durations
    :type (cl:vector cl:fixnum)
   :initform (cl:make-array 0 :element-type 'cl:fixnum :initial-element 0)))
)

(cl:defclass Song-request (<Song-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Song-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Song-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name irobot_mudd-srv:<Song-request> is deprecated: use irobot_mudd-srv:Song-request instead.")))

(cl:ensure-generic-function 'notes-val :lambda-list '(m))
(cl:defmethod notes-val ((m <Song-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader irobot_mudd-srv:notes-val is deprecated.  Use irobot_mudd-srv:notes instead.")
  (notes m))

(cl:ensure-generic-function 'durations-val :lambda-list '(m))
(cl:defmethod durations-val ((m <Song-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader irobot_mudd-srv:durations-val is deprecated.  Use irobot_mudd-srv:durations instead.")
  (durations m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Song-request>) ostream)
  "Serializes a message object of type '<Song-request>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'notes))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:write-byte (cl:ldb (cl:byte 8 0) ele) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) ele) ostream))
   (cl:slot-value msg 'notes))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'durations))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:write-byte (cl:ldb (cl:byte 8 0) ele) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) ele) ostream))
   (cl:slot-value msg 'durations))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Song-request>) istream)
  "Deserializes a message object of type '<Song-request>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'notes) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'notes)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:aref vals i)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:aref vals i)) (cl:read-byte istream)))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'durations) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'durations)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:aref vals i)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:aref vals i)) (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Song-request>)))
  "Returns string type for a service object of type '<Song-request>"
  "irobot_mudd/SongRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Song-request)))
  "Returns string type for a service object of type 'Song-request"
  "irobot_mudd/SongRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Song-request>)))
  "Returns md5sum for a message object of type '<Song-request>"
  "bbc1fa4f04d9b59e8fef37ab5483bbb7")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Song-request)))
  "Returns md5sum for a message object of type 'Song-request"
  "bbc1fa4f04d9b59e8fef37ab5483bbb7")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Song-request>)))
  "Returns full string definition for message of type '<Song-request>"
  (cl:format cl:nil "uint16[] notes~%uint16[] durations~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Song-request)))
  "Returns full string definition for message of type 'Song-request"
  (cl:format cl:nil "uint16[] notes~%uint16[] durations~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Song-request>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'notes) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 2)))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'durations) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 2)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Song-request>))
  "Converts a ROS message object to a list"
  (cl:list 'Song-request
    (cl:cons ':notes (notes msg))
    (cl:cons ':durations (durations msg))
))
;//! \htmlinclude Song-response.msg.html

(cl:defclass <Song-response> (roslisp-msg-protocol:ros-message)
  ((success
    :reader success
    :initarg :success
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass Song-response (<Song-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Song-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Song-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name irobot_mudd-srv:<Song-response> is deprecated: use irobot_mudd-srv:Song-response instead.")))

(cl:ensure-generic-function 'success-val :lambda-list '(m))
(cl:defmethod success-val ((m <Song-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader irobot_mudd-srv:success-val is deprecated.  Use irobot_mudd-srv:success instead.")
  (success m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Song-response>) ostream)
  "Serializes a message object of type '<Song-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'success) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Song-response>) istream)
  "Deserializes a message object of type '<Song-response>"
    (cl:setf (cl:slot-value msg 'success) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Song-response>)))
  "Returns string type for a service object of type '<Song-response>"
  "irobot_mudd/SongResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Song-response)))
  "Returns string type for a service object of type 'Song-response"
  "irobot_mudd/SongResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Song-response>)))
  "Returns md5sum for a message object of type '<Song-response>"
  "bbc1fa4f04d9b59e8fef37ab5483bbb7")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Song-response)))
  "Returns md5sum for a message object of type 'Song-response"
  "bbc1fa4f04d9b59e8fef37ab5483bbb7")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Song-response>)))
  "Returns full string definition for message of type '<Song-response>"
  (cl:format cl:nil "bool success~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Song-response)))
  "Returns full string definition for message of type 'Song-response"
  (cl:format cl:nil "bool success~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Song-response>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Song-response>))
  "Converts a ROS message object to a list"
  (cl:list 'Song-response
    (cl:cons ':success (success msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'Song)))
  'Song-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'Song)))
  'Song-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Song)))
  "Returns string type for a service object of type '<Song>"
  "irobot_mudd/Song")