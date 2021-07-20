#Encompassing Interval method with test cases. Will be updated to work with orderedTree objects.

#Test Cases:
interval = [1, 2]
interval2 = [3, 4]

tree = {1:[2,4,5,6], 3:[4]}

#tree that has nested subtrees
tree2 = {1:[2,5,6,7],3:[5], 4:[5]}
intervalT2 = [3,5]

tree3 = {1:[2,5,6,7],3:[4,5]}
intervalT3 = [3,4]

tree4 = {1:[2,6,7,8],3:[4,6],5:[6]}
intervalT4 = [5,6]
#Encompassing Interval Method:
def encompassingInterval(tree, interval):
  print('\n Interval: ', interval, '\n Ordered Tree: ', tree)
  inKey = interval[0]
  inVal = interval[1]

  #tree1 = orderedTree.orderedTree(5)
  prevKey = 1
  
  for value in tree[inKey]: #tree1.Intervals[inKey]:
      if value > inVal:
        return f"[{inKey}, {value}]"

  for i in tree.keys():
    if i == inKey:
      break
    else:
      prevKey = i
  
  return f"[{prevKey}, {inVal}]"

print(encompassingInterval(tree, interval))
print(encompassingInterval(tree, interval2))
print(encompassingInterval(tree2, intervalT2))
print(encompassingInterval(tree3, intervalT3))
print(encompassingInterval(tree4, intervalT4))
