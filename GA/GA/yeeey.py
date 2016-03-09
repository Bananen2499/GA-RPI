import time, threading, CommandHandler, MotorClass, ServoClasses, CarSocket, sys, random, socket
class cli(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.csock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
    def run(self):
        self.csock.connect(("localhost",25566))
        print("recived: ",self.recivePack())

    def recivePack(self, MSGLEN = 11):
        rec_bytes = self.csock.recv(MSGLEN)
        text = rec_bytes.decode()
        pack = text.split(" ")
        packedInts = [int(pack[0]),int(pack[1]),int(pack[2])]
        return packedInts

        

class host(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.hsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.hsock.bind(("localhost",25566))

    def run(self):
        self.hsock.listen(5)
        print("listens")
        self.sock,adress = self.hsock.accept()
        print("connected")
        text = "128 255 0"
        array = [127,128,219]
        print("sent: ", array)
        sentSize = self.sendPack(array)
        time.sleep(0.1)
        print("size:",sentSize)
        

    def sendPack(self,pack):
        text = str(pack[0])
        for i in range(1,3):
            text = text + " " + str(pack[i])
        sentBytes = self.sock.send(text.encode())
        return sentBytes


c = cli()
h = host()
h.start()
c.start()
c.join()
h.join()

#n = 128
#print(str(128))
#print(str(128).encode())
#a = str(128).encode()
#print(a.decode())
#b = a.decode()
#c = int(b,10)
#print(c)
#print("-----")
#print(chr(128).encode())
#print(bytes((n,)))
#print(bin(n))
#print(n)
#print(bytes.decode(bytes(n)))
#d = CommandHandler.blankDict()
#d["motor_speed"] = 100
#d["steering_direction"] = 1
#d["steering_position"] = 66
#print(CommandHandler.getAsByteArray(d))
#d = CommandHandler.blankDict()
#d["motor_speed"] = 67
#d["motor_direction"] = 1
#d["steering_direction"] = 1
#d["steering_position"] = 36
#print(CommandHandler.getAsByteArray(d))
#print(CommandHandler.getAsDict([137,12,54]))
