from orderedTree import OrderedTree
#Encompassing Interval method with test cases. Will be updated to work with orderedTree objects.

#Test Cases:
interval = [1, 2]
interval2 = [3, 4]

tree = {1:[2,4,5,6], 3:[4]}

#Tree with nested subtrees case:
tree2 = {1:[2,5,6,7],3:[5], 4:[5]}
intervalT2 = [3,5]

tree3 = {1:[2,5,6,7],3:[4,5]}
intervalT3 = [3,4]

tree4 = {1:[2,6,7,8],3:[4,6],5:[6]}
intervalT4 = [5,6]
#Encompassing Interval Method:
def encompassingInterval(ordTree, interval):
  tree = ordTree.tree
  print('\n Interval: ', interval, '\n Ordered Tree: ', tree)
  inKey = interval[0]
  inVal = interval[1]

  prevKey = 1
  
  for value in tree[inKey]: #tree1.Intervals[inKey]: HERE
      if value > inVal:
        return f"[{inKey}, {value}]"

  for i in tree.keys():
    if i == inKey:
      break
    else:
      prevKey = i
  
  print("",f"Encompassing Interval: [{prevKey}, {inVal}]")
  return [prevKey, inVal]


#Rotate Right Method: (IN PROGRESS)
def rotateRight(tree, interval):
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
  for i in tree[encKey]:  
    if i > encVal:
      nextVal = i
      break
  
  tree[encKey].remove(interval[1])  #encompassing interval won't exist after a rotation; deleted here
  #this if statement assures we are creating a new encompassing interval for our new tree after a right rotation
  if interval[0] in tree.keys():
    tree[interval[0]].append(nextVal)
  else:
    tree[interval[0]] = [nextVal]
  #While I don't think we'll have problems appending to lists in our dicts, I could be wrong; I use sort() just in case.
  tree[interval[0]].sort()
  #Print tree after rotation
  print("", "New Ordered Tree:", tree)
  print("-----")

#Test encompassingInterval
encompassingInterval(tree, interval2)
encompassingInterval(tree2, intervalT2)
encompassingInterval(tree3, intervalT3)
encompassingInterval(tree4, intervalT4)

#Test rotatingRight
rotateRight(tree, interval2)
