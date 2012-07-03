; Auto-generated. Do not edit!


(cl:in-package ardrone2_mudd-srv)


;//! \htmlinclude Config-request.msg.html

(cl:defclass <Config-request> (roslisp-msg-protocol:ros-message)
  ((command
    :reader command
    :initarg :command
    :type cl:string
    :initform ""))
)

(cl:defclass Config-request (<Config-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Config-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Config-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name ardrone2_mudd-srv:<Config-request> is deprecated: use ardrone2_mudd-srv:Config-request instead.")))

(cl:ensure-generic-function 'command-val :lambda-list '(m))
(cl:defmethod command-val ((m <Config-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ardrone2_mudd-srv:command-val is deprecated.  Use ardrone2_mudd-srv:command instead.")
  (command m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Config-request>) ostream)
  "Serializes a message object of type '<Config-request>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'command))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'command))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Config-request>) istream)
  "Deserializes a message object of type '<Config-request>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'command) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'command) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Config-request>)))
  "Returns string type for a service object of type '<Config-request>"
  "ardrone2_mudd/ConfigRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Config-request)))
  "Returns string type for a service object of type 'Config-request"
  "ardrone2_mudd/ConfigRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Config-request>)))
  "Returns md5sum for a message object of type '<Config-request>"
  "2fb3aa2736d70ecbfc297d3d9b879661")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Config-request)))
  "Returns md5sum for a message object of type 'Config-request"
  "2fb3aa2736d70ecbfc297d3d9b879661")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Config-request>)))
  "Returns full string definition for message of type '<Config-request>"
  (cl:format cl:nil "string command~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Config-request)))
  "Returns full string definition for message of type 'Config-request"
  (cl:format cl:nil "string command~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Config-request>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'command))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Config-request>))
  "Converts a ROS message object to a list"
  (cl:list 'Config-request
    (cl:cons ':command (command msg))
))
;//! \htmlinclude Config-response.msg.html

(cl:defclass <Config-response> (roslisp-msg-protocol:ros-message)
  ((result
    :reader result
    :initarg :result
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass Config-response (<Config-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Config-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Config-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name ardrone2_mudd-srv:<Config-response> is deprecated: use ardrone2_mudd-srv:Config-response instead.")))

(cl:ensure-generic-function 'result-val :lambda-list '(m))
(cl:defmethod result-val ((m <Config-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ardrone2_mudd-srv:result-val is deprecated.  Use ardrone2_mudd-srv:result instead.")
  (result m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Config-response>) ostream)
  "Serializes a message object of type '<Config-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'result) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Config-response>) istream)
  "Deserializes a message object of type '<Config-response>"
    (cl:setf (cl:slot-value msg 'result) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Config-response>)))
  "Returns string type for a service object of type '<Config-response>"
  "ardrone2_mudd/ConfigResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Config-response)))
  "Returns string type for a service object of type 'Config-response"
  "ardrone2_mudd/ConfigResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Config-response>)))
  "Returns md5sum for a message object of type '<Config-response>"
  "2fb3aa2736d70ecbfc297d3d9b879661")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Config-response)))
  "Returns md5sum for a message object of type 'Config-response"
  "2fb3aa2736d70ecbfc297d3d9b879661")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Config-response>)))
  "Returns full string definition for message of type '<Config-response>"
  (cl:format cl:nil "bool result~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Config-response)))
  "Returns full string definition for message of type 'Config-response"
  (cl:format cl:nil "bool result~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Config-response>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Config-response>))
  "Converts a ROS message object to a list"
  (cl:list 'Config-response
    (cl:cons ':result (result msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'Config)))
  'Config-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'Config)))
  'Config-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Config)))
  "Returns string type for a service object of type '<Config>"
  "ardrone2_mudd/Config")