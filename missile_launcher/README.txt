For first time use:
-------------------
Run the command

rosmake missile_launcher

to setup this package for use on your computer. You have to do this on every new computer that you download the package on.



Instructions:
-------------
To operate the missile launcher, first call

sudo chmod -R 777 /dev/bus/usb/

which will remove the restrictions on accessing the serial port. Then run

rosrun missile_launcher ml_driver.py

to begin advertising the services that control the missile launcher. Currently, a command line does not appear, and all missile launcher control must be done by using

rosservice call SERVICE

or writing a python script. The avaiable services for the missile launcher are:

panR
panL
tiltUp
tiltDown
fire
stop

Every service takes NO ARGUMENTS. There is a small sample python script provided in the scripts directory that demonstrates a simple call to the fire service. Just make sure that the missile launcher isn't pointing at anyone before you try it...
