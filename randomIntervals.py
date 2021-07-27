import random
import orderedTree

def randomInterval(min, max=None):
    """Takes a min and max, returns intervals after splitting on random midpoint"""
  Interval = []
  if max != None:
    Interval = [min, max]
  else:
    Interval = [min, min]

  if (min+1>=max or max==None):
    return None
  
  mid = random.randint(min+1, max-1)
  if(min+1==mid):
      Interval=[mid,max]
      return Interval
  elif(mid+1 == max):
      Interval=[min,mid]
      return Interval
  else:
      Interval = [min,mid]
      interval2 = [mid+1,max]
      return Interval,interval2

def randOrdered(n):
    """Given n leaves, returns a randomly generated orderedTree object"""
  lst = [[1,n]]
  i = 0
  returnCondition = False
  while not returnCondition:
    subIntervals = randomInterval(lst[i][0], lst[i][1])
    if subIntervals == None:
      pass
    elif len(subIntervals) == 1:
      lst.append(subIntervals)
    else:
      for item in subIntervals:
        if isinstance(item, list):
          lst.append(item)
        else:
          lst.append(subIntervals)
          break
    if i == len(lst) - 1:
        returnCondition = True
    i+=1
  oTree = orderedTree[lst]
  return oTree
