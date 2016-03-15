import time, threading, CommandHandler, MotorClass, ServoClasses, CarSocket, sys, random
import RPi.GPIO as io

class master(threading.Thread):
    def __init__(self):
            threading.Thread.__init__(self)
            ##"simulatorns grund"##
            ##first thing to run##
            #self.socket = dummySocket("test.se",15,self)
            ##^ska bytas ut##
            self.socket = CarSocket.CarSocket(parent = self)
            #self.socket.connect("localhost",25566)
            self.socket.hostServerSocket(hostname="192.168.0.117", port=25565)
            self.setDaemon(True)
            self.socket.setDaemon(True)
            

            io.setmode(io.BCM)
            self.dict = self.oldDict= CommandHandler.blankDict()
            #self.motor = MotorClass.DCMotorClass(17,18,500,100,io) #for dc, not used on new car.

            self.motor = MotorClass.StepperMotor(17,18,15,14,1,io)
            self.motor.setDaemon(True)
            self.motor.start()
            self.servo = ServoClasses.ServoClass(27,100,io)
        
    def start(self):
        threading.Thread.start(self)
        self.socket.start()

    def run(self):
        print("lol")
        try:
            #monitor = Monitor(self)
            while 1:
                #print(self.dict)
                self.executeCommands()
                #self.printCommand()
                if time.time() -5 > self.dict["time"]:
                    io.cleanup()
                    raise("stopping")
                    #monitor.start()
                time.sleep(0.08)
        except:
            print("all them exeptions")
            io.cleanup()
            raise("error")

    def executeCommands(self):
        tdict = self.dict
        self.motor.exe(tdict["motor_direction"],tdict["motor_speed"])
        self.servo.exe(tdict["steering_direction"],tdict["steering_position"])
        self.oldDict=tdict

    def printCommand(self):
        tdict = self.dict
        if tdict is not self.oldDict:
            print("----------------------")
            for k in tdict:
                print(k, tdict[k])
            print(CommandHandler.getAsByteArray(tdict))
        self.oldDict = tdict

    def stop():
       print("stop") 

    def __del__(self):
        ##delete everything##
        io.cleanup()
        print("bort")

class Monitor(threading.Thread):
    def __init__(self,parent):
        threading.Thread.__init__(self)
        self.parent = parent
        self.running=False
    def runt(self):
        self.running = True
        d = self.parent.dict
        for x in range(5):
            if (d[time] is not parent.dict[time] and d[time] is  not CommandHandler.validDict(parent.dict)):
                Monitor.shutdown()
            time.sleep(1)
        print("new dict detected")
        print("exiting Monitor")
        self.running = False
    def shutdown(self):
        print("shut down")

class dummySocket(threading.Thread):
    def __init__(self,ip,port,parent):
        threading.Thread.__init__(self)
        self.name = "dummySocket"
        self.ip = ip
        self.port = port
        self.parent = parent
        
    def run(self):
        self.running = True
        while self.running:
            print("do random dict")
            t = [random.randint(128,255),random.randint(0,255),random.randint(0,255)]
            self.parent.dict = CommandHandler.getAsDict(t)
            time.sleep(2)
        
    def stop(self):
        self.running = False
        self.join()


m = master()
m.start()
try:
	while True:
		pass
except KeyboardInterrupt:
	print("Shutting down")
	


def inRange(a,b, x):
    if (x>a and x<b):
        return True
    else:
        return False



