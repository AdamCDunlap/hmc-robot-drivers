
(cl:in-package :asdf)

(defsystem "ardrone2_mudd-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "Config" :depends-on ("_package_Config"))
    (:file "_package_Config" :depends-on ("_package"))
    (:file "Control" :depends-on ("_package_Control"))
    (:file "_package_Control" :depends-on ("_package"))
  ))