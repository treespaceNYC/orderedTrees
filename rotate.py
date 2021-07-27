from orderedTree import orderedTree
#Encompassing Interval method with test cases. Will be updated to work with orderedTree objects.

#Test Cases:
interval = [1, 2]
interval2 = [3, 4]

tree = orderedTree()
tree.intervals = {1:[2,4,5,6], 3:[4]}

#Tree with nested subtrees case:
tree2 = orderedTree()
tree2.intervals = {1:[2,5,6,7],3:[5], 4:[5]}
intervalT2 = [3,5]

tree3 = orderedTree()
tree3.intervals = {1:[2,5,6,7],3:[4,5]}
intervalT3 = [3,4]

tree4 = orderedTree()
tree4.intervals = {1:[2,6,7,8],3:[4,6],5:[6]}
intervalT4 = [5,6]

tree_1 = orderedTree()
tree_1.intervals = {1:[2,3,4,5]}
tree_int1 = [1,2]

tree_2 = orderedTree()
tree_2.intervals = {1:[2,4,5,6],3:[4]}
tree_int2 = [3,4]

tree_3 = orderedTree()
tree_3.intervals = {1:[2,5,6,7],3:[5], 4:[5]}
tree_int3 = [4,5]

tree_4 = orderedTree()
tree_4.intervals = {1:[2,5,6,7],3:[4,5]}
tree_int4 = [3,4]

tree_5 = orderedTree()
tree_5.intervals = {1:[2,5,7],3:[4,5],6:[7]}
tree_int5 = [6,7]

tree_6 = orderedTree()
tree_6.intervals = {1:[2,5,6],3:[4,5,6], 7:[8]}
tree_int6 = [3,4]

tree_7 = orderedTree()
tree_7.intervals = {1:[2,6,8],3:[4,6],5:[6], 7:[8]}
tree_int7 = [3,4]

tree_8 = orderedTree()
tree_8.intervals = {1:[2,10],3:[4,10], 5:[6,7,8],9:[10]}
tree_int8 = [3,4]

tree_9 = orderedTree()
tree_9.intervals = {1:[2,3,14], 4:[14], 5:[11,12,13,14], 6:[7], 8:[9], 10:[11]}
tree_int9 = [5,14]


#Encompassing Interval Method:
def encompassingInterval(ordTree, interval):
  """ Given an orderedTree object and an interval, return the smallest interval encasing input interval. """
  tree = ordTree.intervals
  print('\n Interval: ', interval, '\n Ordered Tree: ', tree)
  inKey = interval[0]
  inVal = interval[1]

  #tree1 = orderedTree.orderedTree(5)
  prevKey = 1
  
  for value in tree[inKey]: #tree1.Intervals[inKey]:
      if value > inVal:
        print(f"Encompassing Interval: [{inKey}, {value}]")
        return f"[{inKey}, {value}]"

  for i in tree.keys(): #
    if i == inKey:
      break
    else:
      for elem in tree[i]:
        if elem == inVal:
          prevKey = i


#Rotate Right Method: (IN PROGRESS i.e. the current method only works under 'ideal' scenarios; the method works when a rotation is possible)
def rotateRight(tree, interval):
  """ Given a tree and interval, rotate interval to a right subtree if possible. """
  #Call encompassingInterval
  #Print tree dict, and interval list
  #Dict for TESTING purposes, CHANGE to orderedTree object BEFORE pr
  print("-----")
  print("", "rotateRight method starts here: ")
  encInterval = encompassingInterval(tree, interval)
  encKey = encInterval[0] #min of encompassing interval
  encVal = encInterval[1] #min of encompassing interval
  #JOYCE CODE HERE

  nextVal = encVal  #max of nearest 'right' subtree to encompassing interval; initiated at encomp interval max for now
  #this for loop will set nextVal to max of nearest 'right' subtree to encompassing interval
  for i in tree.intervals[encKey]:  
    if i > encVal:
      nextVal = i
      break
  
  tree.intervals[encKey].remove(interval[1])  #encompassing interval won't exist after a rotation; deleted here
  #this if statement assures we are creating a new encompassing interval for our new tree after a right rotation
  if interval[0] in tree.intervals.keys():
    tree.intervals[interval[0]].append(nextVal)
  else:
    tree.intervals[interval[0]] = [nextVal]
  #While I don't think we'll have problems appending to lists in our dicts, I could be wrong; I use sort() just in case.
  tree.intervals[interval[0]].sort()
  #Print tree after rotation
  print("", "New Ordered Tree:", tree.intervals)
  print("-----")

#Test encompassingInterval
encompassingInterval(tree, interval2)
encompassingInterval(tree2, intervalT2)
encompassingInterval(tree3, intervalT3)
encompassingInterval(tree4, intervalT4)

encompassingInterval(tree_1, tree_int1)
encompassingInterval(tree_2, tree_int2)
encompassingInterval(tree_3, tree_int3)
encompassingInterval(tree_4, tree_int4)
encompassingInterval(tree_5, tree_int5)
encompassingInterval(tree_6,tree_int6)
encompassingInterval(tree_7,tree_int7)
encompassingInterval(tree_8,tree_int8)
encompassingInterval(tree_9, tree_int9)

#Test rotatingRight
rotateRight(tree, interval2)
