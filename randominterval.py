import random
def randomInterval(min, max=None):
    
    mid = 3
    if (min+1==max):
     return None
    elif(min==mid):
        Interval=[mid+1,max]
        return Interval
    else:
        Interval = [min,mid]
        interval2 = [mid+1,max]
        return Interval,interval2
print (randomInterval(1,5))
