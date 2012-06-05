
(cl:in-package :asdf)

(defsystem "ardrone_mudd-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "navData" :depends-on ("_package_navData"))
    (:file "_package_navData" :depends-on ("_package"))
  ))