from collections import OrderedDict, defaultdict
import re
from shapely.geometry import Polygon
from shapely.geometry import LineString
import math
import random
import matplotlib.pyplot as plt
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
            if(n[0] <= 1):
                self.min = n[0]
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

    def getValences(self):
        """ Gets the valences of an orderedTree object and returns it as a list """

        # Create list to hold valences
        valences = [0]*(self.max+1)
        for key,val in self.intervals.items():
            for i in val:
                # add left interval to valence[interval-1]
                valences[key-1]+=1
                # add right interval to valence[interval]
                valences[i]+=1

        # remove interval [min,max]
        valences[0]-=1
        valences[self.max]-=1
        return valences
    def getSummedValences(self, tree):
        """ Takes two trees and return the a list of the summedvalences """
        # Trees arent the same amount of leaves
        if tree.leaves != self.leaves:
            return None

        # get the valences of the two trees
        left = tree.getValences()
        right = self.getValences()

        # add the two lists
        return [ left[i]+right[i] for i in range(len(left)) ]

    def drawPolygon(tree, **kwargs):
        """ Draws Triangulated Polygon from orderedTree object """
        # possible attributes: placement=, color=, style=, thickness=, innerColor=, outerColor=, innerStyle=, outerStyle=, innerThickness=, outerThickness
        r = lambda: random.randint(0,255)
        rand_color=('#%02X%02X%02X' % (r(),r(),r()))
        #default values
        innerColor=rand_color
        outerColor=rand_color
        innerStyle= '-'
        outerStyle= '-'
        innerThickness= 2
        outerThickness= 2
        placement=0
        #kwargs
        if 'placement' in kwargs:
            placement=kwargs['placement']
        plt.rcParams["figure.figsize"] = [placement*12+5,5] #the dimensions of plot
        if 'color' in kwargs:
            innerColor=kwargs['color']
            outerColor=kwargs['color']
        if 'thickness' in kwargs:
            innerThickness=kwargs['thickness']
            outerThickness=kwargs['thickness']
        if 'style' in kwargs:
            innerStyle=kwargs['style']
            outerStyle=kwargs['style']
        if 'innerColor' in kwargs:
            innerColor=kwargs['innerColor']
        if 'outerColor' in kwargs:
            outerColor=kwargs['outerColor']
        if 'innerStyle' in kwargs:
            innerStyle=kwargs['innerStyle']
        if 'outerStyle' in kwargs:
            outerStyle=kwargs['outerStyle']
        if 'innerThickness' in kwargs:
            innerThickness=kwargs['innerThickness']
        if 'outerThickness' in kwargs:
            outerThickness=kwargs['outerThickness']
        #if innerColor but no outerColor
        if 'innerColor' in kwargs and 'outerColor' not in kwargs:
            outerColor=kwargs['innerColor']
        #if outerColor but no innerColor
        if 'outerColor' in kwargs and 'innerColor' not in kwargs:
            innerColor=kwargs['outerColor']
        n=tree.leaves
        sides=tree.leaves+1
        r=3    #radius size of shape
        angle=(2*math.pi)/(sides)
        vertices=[]
        start=math.ceil(sides/2)
        offset=placement*7-7 #changes the X value of the points
        # get points for vertices of polygon
        for i in range(start,sides):
            if sides%2==0:
                x = r * math.sin(i * angle+math.pi/sides) +offset
                y = -(r * math.cos(i * angle+math.pi/sides)) #negate y value to flip the polygon
                vertices.append((x,y))
            else:
                x = r * math.sin(i * angle) +offset
                y = -(r * math.cos(i * angle)) #negate y value to flip the polygon
                vertices.append((x,y))
        for i in range(0,start):
            if sides%2==0:
                x = r * math.sin(i * angle+math.pi/sides)+offset
                y = -(r * math.cos(i * angle+math.pi/sides)) #negate y value to flip the polygon
                vertices.append((x,y))
            else:
                x = r * math.sin(i * angle)+offset
                y = -(r * math.cos(i * angle)) #negate y value to flip the polygon
                vertices.append((x,y))
        #draw the internal edges
        intervals = tree.intervals
        for key, val in intervals.items():
            for i in val:
                if (key==1 and i==n):
                    #make the top edge (the min,max interval) thicker
                    topEdge = LineString([vertices[0], vertices[-1]])
                    plt.plot(*topEdge.xy,color=outerColor,linewidth=5)
                else:
                    line = LineString([vertices[key-1], vertices[i]])
                    plt.plot(*line.xy,color=innerColor, linestyle=innerStyle, linewidth=innerThickness)
        #create polygon using the vertices found above
        polygon1 = Polygon(vertices)
        #plot polygon
        x, y = polygon1.exterior.xy
        plt.plot(x, y, color=outerColor, linestyle=outerStyle, linewidth=outerThickness)

def dictToInt(my_dict):
    """ Returns a list of intervals after converting from dictionary format """
    lst = []
    for key,item in my_dict.items():
        for i in item:
            lst.append([key,i])

    return lst

def removeSiblings(tree, tree1):#non member
    """ Compares two trees and returns a list of two trees with their common sibling pairs removed """
    # ========= Get valences ========= #
    valences = tree.getSummedValences(tree1)
    
    # Check if trees are not the same size
    if not valences:
        return None
    # Check if only sibling pairs in tree
    if [0]*len(valences)==valences:
        return [orderedTree(), orderedTree()]

    # Get all pairs to remove
    pos = []
    for i in range(len(valences)-1):
        if valences[i] == 0:
            pos.append(i+1)
    
    # ========= Cleanup ========= #
    if len(pos)==0:
        return None

    # Edge Case
    if pos[-1] == tree.max+1:
        pos[-1] = tree.max

    # ========= Delete ========= #
    selfIntervals = dictToInt(tree.intervals)
    treeIntervals = dictToInt(tree1.intervals)

    # Loop through pairs and remove them from intervals
    for i in pos:
        selfIntervals.remove([i-1,i])
        treeIntervals.remove([i-1,i])
    
    if pos[-1] == tree.max:
        pos = pos[:-1]

    # ========= Shift ========= #

    # Loop through each interval
    # If greater than removed pair, shift num down 1
    for j in range(len(selfIntervals)):
        for i in range(len(pos),0,-1):
            if selfIntervals[j][0]>=pos[i-1]:
                selfIntervals[j][0]-=1
            if selfIntervals[j][1]>=pos[i-1]:
                selfIntervals[j][1]-=1


            if treeIntervals[j][0]>=pos[i-1]:
                treeIntervals[j][0]-=1
            if treeIntervals[j][1]>=pos[i-1]:
                treeIntervals[j][1]-=1
    
    return [orderedTree(selfIntervals), orderedTree(treeIntervals)]
        
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
