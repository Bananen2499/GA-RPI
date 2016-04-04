class ServoClass(object):
    """Servoclass for analog servo"""

    def __init__(self,pin,bound,io):
        self.bound = bound
        io.setup(27,io.OUT)
        self.servo = io.PWM(27,50)
        dc = calcDc(0)
        self.servo.start(dc)
        #stuff needed to be added

    
    def pos(self,p):
        self.servo.ChangeFrequency(50) #a bugg keeps changing it
        dc = calcDc(p)
        self.servo.ChangeDutyCycle(dc)
        print("pos ",p)

    def exe(self,dir,pos):
        pos = (pos/128) * self.bound
        if (abs(pos) <= self.bound):
            if (dir == 0):
                self.pos(-pos)
            else:
                self.pos(pos)
        else:
            print("Servo out of range!")

    def __del__(self):
        self.servo.stop()
    #more stuff added later on rpi.


def calcDc(direction):
    return (7 + (direction / 100 * 5.5))

