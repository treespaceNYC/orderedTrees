import random
def randomInterval(min, max=None):
    
    mid = random.randint(min, max-1)
    if (min+1==max):
     return None
    elif(min==mid):
        Interval=[mid+1,max]
        return Interval
    elif(min+2==max):
        Interval=[min,min+1]
        return Interval
    else:
        Interval = [min,mid]
        interval2 = [mid+1,max]
        return Interval,interval2
print (randomInterval(5,10))
