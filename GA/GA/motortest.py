import RPi.GPIO as io
import time, threading, MotorClass,CommandHandler
io.setmode(io.BCM)
motor = MotorClass.StepperMotor(17,18,15,14,1,io)
motor.setDaemon(True)
motor.start()
print("starting")
inp = "123"
while inp.isalpha:
    print("set speed")
    inp = input()
    self.motor.exe(1,int(inp))
print("exitiong")
io.cleanup()
