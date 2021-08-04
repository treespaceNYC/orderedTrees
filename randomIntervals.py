import random
from OrderedTree import OrderedTree

# Parameters can be either two ints or just one list
def randInterval(min, max=None):
    """ Takes a min and max, returns intervals after splitting on random midpoint """
    interval = []

    # If input is (list,None)
    if max == None:
        max = min[1]
        min = min[0]

    # If impossible to make sub-interval ex: [1,2]
    if (min + 1 >= max):
        return None

    # Ex: [1,3] 2 is mid, choose [1,2] or [2,3]
    if(min +2 == max):
        return random.choice([[[min,min+1]],[[min+1,max]]])

    # Choose random midpoint
    mid = random.randrange(min+1, max)

    # If mid is 1 away from max, choose one possibility 
    if mid+1==max:
        return random.choice( ([[min,mid]] , [[min,mid-1],[mid,max]]) )

    # Return two split sub-intervals
    interval = [min,mid]
    interval2 = [mid+1,max]
    return [interval,interval2]

def randOrdered(n):
    """ Given n leaves, returns a randomly generated OrderedTree object """
    # Edge cases with impossible intervals
    if n<=1:
        return OrderedTree()

    lst = [[1,n]]
    i = 0

    # Loop until all intervals are made
    while i != n-1:
        subIntervals = randInterval(lst[i]) # Create random intervals
        # Do nothing if interval is [x,x+1] ex: [1,2]
        if subIntervals == None:
            pass
        # Append 1 random interval to lst
        elif len(subIntervals) == 1:
            lst.append(subIntervals[0])
        # Append both random intervals to lst
        else:
            lst.append(subIntervals[0])
            lst.append(subIntervals[1])
        
        # Move lst iterator by 1
        i+=1

    # Create new tree from random list
    oTree = OrderedTree(sorted(lst))
    return oTree
