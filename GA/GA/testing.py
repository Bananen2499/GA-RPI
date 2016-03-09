import math
def calcDelay(current,wanted):
    if wanted == -1:
        return -1
    
    x = abs(wanted/current) *(wanted-current)+current
    return round(x,2)

print(calcDelay(15,10))
print(calcDelay(15,15))
print(calcDelay(15,15))

last = 50
for i in range(50,0,-5):
    last = 50
    for j in range(5):
        print(calcDelay(last,i)," : ",i," : ",last)
        last = calcDelay(last,i)
