import random
from orderedTree import orderedTree

def randInterval(min, max=None):
    """Takes a min and max, returns intervals after splitting on random midpoint"""
    interval = []
    if max != None:
        interval = [min, max]
    else:
        interval = min
        min = interval[0]
        max = interval[1]
    if (min+1>=max):
        return None
    if(min +2 == max):
        return random.choice([[[min,min+1]],[[min+1,max]]])
    mid = random.randrange(min+1, max-1)
    interval = [min,mid]
    interval2 = [mid+1,max]
    return [interval,interval2]

def randOrdered(n):
    """Given n leaves, returns a randomly generated orderedTree object"""
    if(n<=1):
        return orderedTree()
    lst = [[1,n]]
    i = 0
    while i != n-1:
        subIntervals = randInterval(lst[i])
        if subIntervals == None:
            pass
        elif len(subIntervals) == 1:
            lst.append(subIntervals[0])
        else:
            lst.append(subIntervals[0])
            lst.append(subIntervals[1])
        i+=1
    oTree = orderedTree(lst)
    oTree
    return oTree

print(randInterval([1,3]))
