
import RPi.GPIO as io
import time

io.setmode(io.BCM)

coil_A_pin = 17
coil_B_pin = 18
coil_C_pin = 15
coil_D_pin = 14

io.setup(coil_A_pin, io.OUT)
io.setup(coil_B_pin, io.OUT)
io.setup(coil_C_pin, io.OUT)
io.setup(coil_D_pin, io.OUT)
def accelerating(delayStart,delayStop):
    print("accelerating")
    for delay in range(delayStart,delayStop,-1):
        print(delay)
        for i in range(0,int (1000/delay)):
            setStep(1,0,1,0)
            time.sleep(delay/1000)
            setStep(0,1,1,0)
            time.sleep(delay/1000)
            setStep(0,1,0,1)
            time.sleep(delay/1000)
            setStep(1,0,0,1)
            time.sleep(delay/1000)
    print("stopping")
    setStep(0,0,0,0)


def setStep(w1,w2,w3,w4):
    io.output(coil_A_pin,w1)
    io.output(coil_B_pin,w2)
    io.output(coil_C_pin,w3)
    io.output(coil_D_pin,w4)

def forward(delay,steps):
    print("starting")
    for i in range(0,steps):
        setStep(1,0,1,0)
        time.sleep(delay)
        setStep(0,1,1,0)
        time.sleep(delay)
        setStep(0,1,0,1)
        time.sleep(delay)
        setStep(1,0,0,1)
        time.sleep(delay)
    print("done")
    setStep(0,0,0,0)

def backward(delay,steps):
    print("back starting")
    for i in range(0,steps):
        setStep(1,0,0,1,)
        time.sleep(delay)
        setStep(0,1,0,1)
        time.sleep(delay)
        setStep(0,1,1,0)
        time.sleep(delay)
        setStep(1,0,1,0)
        time.sleep(delay)
    setStep(0,0,0,0)
while True:
    print("input 'delay steps direction'")
    print("delay is in miliseconds")
    print("1 is forward, 2 is back")

    inp = input()
    if inp.isalpha():
        break
    
    (delay,steps,dir) = inp.split()
    steps = int(steps)
    if (int(dir)==1):
        delay = int(delay)/1000
        forward(delay, steps)
    elif(int(dir)==2):
        delay = int(delay)/1000
        backward(delay,steps)
    elif (int(dir)==3):
        accelerating(int(delay),steps)
    else:
       print("type just letters to exit")
print("exiting")
io.cleanup()


