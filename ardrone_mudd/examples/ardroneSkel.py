import ardrone

class myArdrone(ardrone.Ardrone):
    def __init__(self):
        ardrone.Ardrone.__init__(self)
        self.state = "keyboard"

    def loop(self):
        while True:
            char = drone.getKeyPress()
            if char == 'n':
                print "Hi"

if __name__== "__main__":
  drone = myArdrone()
  print "Ready"
  drone.loop()
