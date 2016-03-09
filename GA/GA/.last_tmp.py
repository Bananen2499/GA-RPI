import time, threading, CommandHandler, MotorClass, ServoClasses, CarSocket, sys, random

class master(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        ##"simulatorns grund"##
        ##first thing to run##
        #self.socket = dummySocket("test.se",15,self)
        ##^ska bytas ut##
        self.socket = CarSocket.CarSocket(parent = self)
        self.socket.connect("148.136.200.190",25566)
        #self.socket.hostServerSocket(hostname="localhost", port=25565)
        print("connected")
        self.setDaemon(True)
        self.socket.setDaemon(True)
        self.dict = self.oldDict= CommandHandler.blankDict()
        #self.motor = MotorClass.MotorClass(17,18,500) 
        #self.servo = ServoClasses.ServoClass(21)
        
    def start(self):
        threading.Thread.start(self)
        self.socket.start()

    def run(self):
        print("Main Thread started")
        monitor = Monitor(self)
        while 1:
            #print(self.dict)    
            self.printCommand()
			if time.time() -5 > self.dict[time]:
					monitor.start()
            time.sleep(5)

    def executeCommand(self):
        tdict = self.dict
        if (tdict["motor_direction"] == 1):
            self.motor.fram(tdict["motor_speed"])
        else:
            self.motor.bak(tdict["motor_speed"])
		




    def printCommand(self):
        tdict = self.dict
        if tdict is not self.oldDict:
            print("----------------------")
            for k in tdict:
                print(k, tdict[k])
            print(CommandHandler.getAsByteArray(tdict))
        self.oldDict = tdict
    def __del__(self):
        ##delete everything##
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
			if (d[time] is not parent.dict[time] and not CommandHandler.validDict(parent.dict)):
				Monitor.shutdown()
			time.sleep(1)
		print("new dict detected")
		print("exiting Monitor")
		self.running = False
    def shutdown(self):
                
		
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
            t = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
            self.parent.dict = CommandHandler.getAsDict(t)
            time.sleep(2)
        
    def stop(self):
        self.running = False
        self.join()


m = master()
m.start()
#try:
while True:
	inp=input()
	print(inp)
	if inp is "dc":
		print("disconnect")
		m.socket.sock.close()
	if inp is "exit":
		print("exits")
		break

#except KeyboardInterrupt:
#	print("Shutting down")
#	m.socket.sock.close()
	

def inRange(a,b, x):
    if (x>a and x<b):
        return True
    else:
        return False