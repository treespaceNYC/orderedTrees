from OrderedTree import OrderedTree
#Encompassing Interval method with test cases. Will be updated to work with OrderedTree objects.

#Test Cases:
interval = [1, 2]
interval2 = [3, 4]

tree = OrderedTree()
tree.intervals = {1:[2,4,5,6], 3:[4]}

#Tree with nested subtrees case:
tree2 = OrderedTree()
tree2.intervals = {1:[2,5,6,7],3:[5], 4:[5]}
intervalT2 = [3,5]

tree3 = OrderedTree()
tree3.intervals = {1:[2,5,6,7],3:[4,5]}
intervalT3 = [3,4]

tree4 = OrderedTree()
tree4.intervals = {1:[2,6,7,8],3:[4,6],5:[6]}
intervalT4 = [5,6]

tree_1 = OrderedTree()
tree_1.intervals = {1:[2,3,4,5]}
tree_int1 = [1,2]

tree_2 = OrderedTree()
tree_2.intervals = {1:[2,4,5,6],3:[4]}
tree_int2 = [3,4]

tree_3 = OrderedTree()
tree_3.intervals = {1:[2,5,6,7],3:[5], 4:[5]}
tree_int3 = [4,5]

tree_4 = OrderedTree()
tree_4.intervals = {1:[2,5,6,7],3:[4,5]}
tree_int4 = [3,4]

tree_5 = OrderedTree()
tree_5.intervals = {1:[2,5,7],3:[4,5],6:[7]}
tree_int5 = [6,7]

tree_6 = OrderedTree()
tree_6.intervals = {1:[2,5,6],3:[4,5,6], 7:[8]}
tree_int6 = [3,4]

tree_7 = OrderedTree()
tree_7.intervals = {1:[2,6,8],3:[4,6],5:[6], 7:[8]}
tree_int7 = [3,4]

tree_8 = OrderedTree()
tree_8.intervals = {1:[2,10],3:[4,10], 5:[6,7,8],9:[10]}
tree_int8 = [3,4]

tree_9 = OrderedTree()
tree_9.intervals = {1:[2,3,14], 4:[14], 5:[11,12,13,14], 6:[7], 8:[9,11], 10:[11]}
tree_int9 = [5,14]


#Encompassing Interval Method:
def encompassingInterval(ordTree, interval):
  """ Given an OrderedTree object and an interval, return the smallest interval encasing input interval. """
  tree = ordTree.intervals
  print('\n Interval: ', interval, '\n Ordered Tree: ', tree)
  inKey = interval[0]
  inVal = interval[1]

  #tree1 = orderedTree.orderedTree(5)
  prevKey = 1
  
  for value in tree[inKey]: #tree1.Intervals[inKey]:
      if value > inVal:
        return [inKey, value]

  for i in tree.keys(): 
    if i == inKey:
      break
    else:
      for elem in tree[i]:
        if elem == inVal:
          prevKey = i
  
  return [prevKey, inVal]


def rotateRight(tree, interval):
  """ Given a tree and interval, rotate interval to a right subtree if possible. """
    #if interval max is not a value in key (it is a min so can't rotate right)
    if(interval[1] not in tree.intervals[interval[0]]):#if the input interval doesnt consist of a real [min max]
        return None
    lonepair = True

    #check if interval max is a lone pair or not
    for key in tree.intervals.keys():##fix to break out of double forloop
        for val in tree.intervals[key]:#check to see if pair is a lone pair, a pair that consists of the max being attached straight to 1, or the absolute min
            if val == interval[1]:#loop through, find the value and check if it is in the key of 1 or the absolute min
                if(key != interval[0]):
                    lonepair = False##lonepair is false if value does not exist in key of absolute min
                    break
                    
    encomp = encompassingInterval(tree, interval)#get encompassing interval
    
    #if lonepair is TRUE
    if(interval[0]+1 == interval[1] or lonepair):#if its a sibling pair, or lonepair
        if(encomp[1] == interval[1]):#make sure if can't rotate
            return None
        #if interval is lone pair
        if(encomp[0] == interval[0]):#if original interval and encompassing interval share a min
            tree.intervals[interval[0]].remove(interval[1])#remove the max from the key
            if(not tree.intervals[interval[0]]):#if the key is now empty not sure if this is necessary
                del tree.intervals[intervals[0]]#delete the key
            tree.intervals.setdefault(interval[1],[encomp[1]])#create a new key with the given interval max and set its value to the encompassing max
            tree.intervals = OrderedDict(sorted(tree.intervals.items()))#sort
        return tree

    #if lonepair is FALSE
    if(interval[0] == encomp[0]):#if min of given interval is the same as min of encompassing, you cannot rotate right
        return None
    elif(interval[1] == tree.max):#if the max of interval is the largest leaf
        return None
    elif(interval[0] == tree.min):#if the min of the interval is the smallest leaf
        return None
    elif(interval[1] == interval[0]):#if the interval min == interval max ie: [2,2]
        return None
    tree.intervals[encomp[0]].remove(encomp[1])#remove the encompassing interval
    if(not (tree.intervals[encomp[0]])):#if its empty, delete the key, not sure if needed
        del tree.intervals[encomp[0]]
    #loop through key of encompassing intervals
    for val in tree.intervals[encomp[0]]:
        if val > interval[1]:
            tree.intervals[interval[0]].append(val)
            return tree

    return None

#Test encompassingInterval
print(encompassingInterval(tree, interval2))
print(encompassingInterval(tree2, intervalT2))
print(encompassingInterval(tree3, intervalT3))
print(encompassingInterval(tree4, intervalT4))

print(encompassingInterval(tree_1, tree_int1))
print(encompassingInterval(tree_2, tree_int2))
print(encompassingInterval(tree_3, tree_int3))
print(encompassingInterval(tree_4, tree_int4))
print(encompassingInterval(tree_5, tree_int5))
print(encompassingInterval(tree_6,tree_int6))
print(encompassingInterval(tree_7,tree_int7))
print(encompassingInterval(tree_8,tree_int8))
print(encompassingInterval(tree_9, tree_int9))


#Test rotatingRight
rotateRight(tree, interval2)
