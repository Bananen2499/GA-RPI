import threading,time,math
class DCMotorClass(object):
    """Motor controller class"""
    def __init__(self,pin1,pin2,frec,bound,io):
        print("motor setting up")
        self.bound = bound
        self.pin1 = pin1
        self.pin2 = pin2
        io.setup(pin1,io.OUT)
        io.setup(pin2,io.OUT)
        self.frec = frec
        self.dir = None
        
        self.mp1 = io.PWM(pin1,frec)
        self.mp2 = io.PWM(pin2,frec)
        #self.mp1.start(0)
        #self.mp2.start(0)

    def runMotor(self,speed):
            #add code on RPI, or whatevs
        #if speed is lower than 50, speed is 50
        self.cf()
        if  (speed > 0 ):
            print("fram")
            if (speed <50):speed = 50
            self.mp1.start(abs(speed))
            #self.mp1.ChangeDutyCycle(abs(speed))
            #self.mp2.ChangeDutyCycle(0)
            self.mp2.stop()
        elif (speed < 0):
            print("bak")
            if (abs(speed) <50):speed = 50
            self.mp1.stop()
            self.mp2.start(abs(speed))
            #self.mp1.ChangeDutyCycle(0)
            #self.mp2.ChangeDutyCycle(abs(speed))
        else:
            self.mp1.stop()
            self.mp2.stop()
        print("speed: ",speed)

    def cf(self,f = None):
        """due to an apparent bug in RPI.GPIO"""
        if (f is None):f = self.frec
        self.mp1.ChangeFrequency(f)
        self.mp2.ChangeFrequency(f)
    
    def exe(self,direc,speed):
        print("org speed:",speed, " : ",direc)
        speed = (speed/128) * self.bound
        if (abs(speed) <= self.bound):
            if (direc == 0):
                speed = -speed
            else:
                speed = speed
            print(speed)
            self.runMotor(speed)
        else:
            print("Motor speed out of set range!")

    def startPWM(self):
        self.mp1.start(0)
        self.mp2.start(0)

    def stop(self):
        self.mp1.stop()
        self.mp2.stop()

    def __del__(self):
        stop()
        print("stop pwm's and delete motorthingies")
        #add code.. nvm..

class StepperMotor(threading.Thread):
    def __init__(self,coil_A_pin,coil_B_pin,coil_C_pin,coil_D_pin,bound,io):
        self.coil_A_pin = coil_A_pin
        self.coil_B_pin = coil_B_pin
        self.coil_C_pin = coil_C_pin
        self.coil_D_pin = coil_D_pin
        #seting up the coils as IO Outputs.
        io.setup(coil_A_pin, io.OUT)
        io.setup(coil_B_pin, io.OUT)
        io.setup(coil_C_pin, io.OUT)
        io.setup(coil_D_pin, io.OUT)
        self.io = io
        #the order that the motor spins in
        self.coilOrder = [[1,0,1,0],[0,1,1,0],[0,1,0,1],[1,0,0,1],[0,0,0,0]]
        #min delay betwen switching
        self.bound = bound
        self.currentDelay = -1 #delay in ms
        self.wantedDelay = -1
        self.direction = 1 #forward
        threading.Thread.__init__(self)
        print("done with init in stepper")

    def setStep(self,configuration):
        self.io.output(self.coil_A_pin,configuration[0])
        self.io.output(self.coil_B_pin,configuration[1])
        self.io.output(self.coil_C_pin,configuration[2])
        self.io.output(self.coil_D_pin,configuration[3])

    def run(self):
        self.running = True
        print("running stepperthread")
        currentCoilConfig = 1 #betwen 0-3
        while self.running:
            
            tempDelay =  self.wantedDelay
            self.currentDelay = tempDelay
            #tempDelay =  self.calcDelay(self.currentDelay,self.wantedDelay)
            #self.currentDelay = tempDelay
            print("current",self.currentDelay,": wanted",self.wantedDelay)            
            if (self.direction < 0) or (tempdelay == -1):
                self.setStep(self.coilOrder[4])
                time.sleep(40/1000)
            elif self.direction ==1:
                for i in range(0,3,1):
                    print(i)
                    self.setStep(self.coilOrder[i])
                    time.sleep(tempDelay/1000)
            else:
                for i in range(3,-1,-1):
                    print(i)
                    self.setStep(self.coilOrder[i])
                    time.sleep(tempDelay/1000)

    def calcDelay(current,wanted):
        return round(abs(wanted/current) *(wanted-current)+current,1)

    def exe(self,direc,speed):
        #thingies
        print("exe stepper")
        self.direction = direc
        if (speed != 0):
            self.wantedDelay = speed * -(39/127) + 40.3
        else:
            self.direction=-1    
    def stop(self):
        self.running = False
    def __del__(self):
        self.running = False
        
    
