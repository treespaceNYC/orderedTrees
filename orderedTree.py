from collections import OrderedDict, defaultdict
import re
#Need to include a way for python to know which constructor to use.

class orderedTree:
    def __init__(self, *n):
        if(len(n) == 0):
            """ Default constructor that creates an empty tree """
            self.leaves = 0
            self.intervals = defaultdict(list)
            self.min=0
            self.max=0

        elif(isinstance(n[0], int)):
            """ Takes an Int and creates a dictionary with intervals[1, 2]...[1, n] """
            self.intervals = defaultdict(list)
            self.leaves = n[0]
            self.min=1
            self.max=n[0]
            for i in range(2,n[0]+1):
                self.intervals[1].append(i)

        elif(isinstance(n[0], list)):
            """ Creates a tree based on a list entered in intervals (List of lists) """
            self.intervals = defaultdict(list)
            self.min=1
            max = 0
            for k, v in n[0]:
                self.intervals[k].append(v)
                if(v > max):
                    max = v
            self.leaves = max
            self.max = max
        elif(isinstance(n[0], str)):
            """ Creates a tree from newick string input """
            self.intervals = newick2interval(n[0])
            self.min = 1
            lst = list(self.intervals.values())
            self.max = lst[-1][0]
            self.leaves = self.max

    def __str__(self):
        """ Allows for printing of dictionary and # of leaves """
        lst = list(zip(self.intervals.keys(), self.intervals.values()))
        return(f"(Dictionary: {lst}\n# of leaves = {self.leaves}\n min = {self.min} \n max = {self.max}")


    def __eq__(self, tree):
        """ Allows for == override """
        if(list(self.intervals.items()) == (list(tree.intervals.items()))):
            return True
        return False

    def commonEdges(self, tree1):
        """ finds common edges between two trees. ex: tree1.commonEdges(tree2) """
        lst = []
        for key in tree1.intervals.keys():
            if(key in self.intervals.keys()):
                for i in tree1.intervals.get(key):
                    for j in self.intervals.get(key):
                        if(i == j):
                            lst.append([key, i])
                            break
        return lst

def interval2newick(interval):
    """ Interval notation to newick notation """
    intervals = defaultdict(list)
    for k, v in interval:
        intervals[k].append(v)
    #turn input into a dictionary
    minMax = {}
    # Using number of values of each key
    # to find how nested it is
    for key, val in intervals.items():
        for i in val:
            minMax.setdefault(key,["(",0])
            #set key to all the min leaves, and then the values to the open paren since we use those b4 mins and then the counter for how many
            minMax.setdefault(i,[")",0])
            #set the key to all the max leaves and then set the values to closing paren and set the counter for the number of closing paren to print

            minMax[i][1]+=1
            #if we see max, we add one to its counter
            minMax[key][1]+=1
            #if we see a value for the min, add one to the counter
    minMax = OrderedDict(sorted(minMax.items()))
    result = ""
    for key, val in minMax.items():
    #formatting what we stored into a string to return
        if val[0] == "(":
            result+= (val[0]*val[1]) + str(key) + ","
        else:
            result+= str(key) + (val[0]*val[1]) + ","
    return result[:-1]

def newick2interval(newick):
    """ Newick format to interval format converter """
    intervals = []
    commaCount = newick.count(",")
    while commaCount!=1:
        m = re.search(",?\(\d+,\d+\),?",newick)
        groupPos = m.span() # tuple in the form (pos, pos)

        # Right sibling pair
        if m.group()[0] == ",":
                # Find position of "," to split string
            commaPos = groupPos[0]+m.group().rindex(",")

            # Left number
            left = int(newick[groupPos[0]+2:commaPos])
            # Right number
            right = int(newick[commaPos+1:groupPos[1]-1])

            # Add to interval then shrink string
            intervals.append([left,right])
            newick = newick[:groupPos[0]+1] + newick[commaPos+1:groupPos[1]-1] + newick[groupPos[1]:]

        # Left sibling pair
        else:
            # Find position of "," to split string
            commaPos = groupPos[0]+m.group().index(",")

            # Left number
            left = int(newick[groupPos[0]+1:commaPos])
            # Right number
            right = int(newick[commaPos+1:groupPos[1]-2])

            # Add to interval then shrink string
            intervals.append([left,right])
            newick = newick[:groupPos[0]] + newick[groupPos[0]+1:commaPos] + newick[groupPos[1]-1:]
        commaCount-=1
    # String is now in the form (\d,\d)

    # Find position of "," to split string
    commaPos = newick.index(",")

    # Left number
    left = int(newick[1:commaPos])
    # Right number
    right = int(newick[commaPos+1:len(newick)-1])

    # Add to interval then turn into dictionary
    intervals.append([left,right])
    d = defaultdict(list)
    for k, v in intervals:
        d[k].append(v)
    return OrderedDict(sorted(d.items()))#sort and return

#Encompassing Interval Method:
def encompassingInterval(ordTree, interval):
  tree = ordTree.intervals
  inKey = interval[0]
  inVal = interval[1]

  prevKey = 1

  for value in tree[inKey]: #tree1.Intervals[inKey]: HERE
      if value > inVal:
        return [inKey, value]

  for i in tree.keys():
    if i == inKey:
      break
    else:
      prevKey = i
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



def getTreeValences(tree):
    """ Gets the valences of an orderedTree object and returns it as a list """
    
    # Create list to hold valences
    valences = [0]*(tree.max+1)
    for key,val in tree.intervals.items():
        for i in val:
            # add left interval to valence[interval-1]
            valences[key-1]+=1
            # add right interval to valence[interval]
            valences[i]+=1
    
    # remove interval [min,max]
    valences[0]-=1
    valences[tree.max]-=1
    return valences


def getSummedValences(tree, tree1):
    # Trees arent the same amount of leaves
    if tree.leaves != tree1.leaves:
        return None
    
    # get the valences of the two trees
    left = getTreeValences(tree)
    right = getTreeValences(tree1)
    
    # add the two lists
    return [ left[i]+right[i] for i in range(len(left)) ]
