import ardrone

class myArdrone(ardrone.Ardrone()):

    def test():
        print "hi"

if __name__== "__main__":
  drone = myArdrone()
  print "Ready"
  while(True):
    drone.getKeyPress()
