from tkinter import *
import time, threading, CommandHandler, MotorClass, ServoClasses, socket, sys, random, CarSocket


class Application(Frame):
    def say_hi(self):
        print("hi there, everyone!")

    def sendCommand(self,dir,speed):
        dict = CommandHandler.blankDict()
        if  (dir <= 0):
            dict["steering_direction"] = 0
            dict["steering_position"] = -dir
        else:
            dict["steering_direction"] = 1
            dict["steering_position"] = dir
        if (speed <= 0):
            dict["motor_direction"] = 0
            dict["motor_speed"] = -speed
        else:
            dict["motor_direction"] = 1
            dict["motor_speed"] = speed
        dict["time"] = int(time.time())
        commandArray = CommandHandler.getAsByteArray(dict)
        print("sending command")
        print("----------------------")
        for k in dict:
            print(k, dict[k])
        print(commandArray)
        self.sock.sendPack(commandArray)


    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "left"})

        self.left = Button(self)
        self.left["text"] = "left",
        self.left["command"] = self.leftC
        
        self.right = Button(self)
        self.right["text"] = "right",
        self.right["command"] = self.rightC
        
        self.forward = Button(self)
        self.forward["text"] = "forward",
        self.forward["command"] = self.fram


        self.back = Button(self)
        self.back["text"] = "back",
        self.back["command"] = self.bak

        self.left.pack({"side": "left"})
        self.right.pack({"side": "left"})
        self.forward.pack({"side": "left"})
        self.back.pack({"side": "left"})

    def fram(self):
        self.sendCommand(0,100)
    def bak(self):
        self.sendCommand(0,-100)

    def rightC(self):
        self.sendCommand(100,0)

    def leftC(self):
        self.sendCommand(-100,0)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.sock = CarSocket.CarSocket(self)
        print("listening")
        self.sock.hostServerSocket("localhost",25566)
        #self.sock.connect("localhost",25566)
        print("ansluten")
        self.pack()
        self.createWidgets()


class SrvSock(object):
    def returnCarSocket(mparent):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(socket.gethostname())
        serversocket.bind(("localhost",25566))
        serversocket.listen(5)
        print("listening")
        carsock = CarSocket.CarSocket(parent = mparent)
        s,adress =serversocket.accept()
        carsock.changeSocketTo(s)
        print("socket ansluiten")
        return carsock

        



root = Tk()
app = Application(master=root)

app.mainloop()
root.destroy()
