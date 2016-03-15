import math
def calcDelay(current,wanted,maxStep):
    if wanted == -1:
        return -1
    if current <0:
        return wanted
    diff = current - wanted
    if maxStep < abs(diff):
        if diff < 0:
            ret = current -maxStep
        else:
            ret = current + maxStep
    else:
        if diff < 0:
            ret = current - diff
        else:
            ret = current + diff        
    x = round(abs(wanted/current) *(wanted-current)+current,1)
    return round(ret,2)

print(calcDelay(15,10,2))
print(calcDelay(15,15,2))
print(calcDelay(15,15,2))
print(calcDelay(-1,50,2))
last =-1
for i in range(50,0,-5):
    last = 50
    for j in range(5):
        print(calcDelay(last,i,2)," : ",i," : ",last," : ",j)
        last = calcDelay(last,i,2)
