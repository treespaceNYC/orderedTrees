from collections import OrderedDict, defaultdict
from shapely.geometry import LineString, Polygon
import copy
import math
import matplotlib.pyplot as plt
import random
import re


class OrderedTree:
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

    def removeCommon(self,tree):
        """ Create two pairs of trees after separating common edges """
        interval = self.commonEdges(tree)

        # Edge case
        if len(interval)==0:
            return None

        # No more common edges
        if interval[0] == [self.min,self.max] and len(interval)==1:
            return None

        # Get first common edge
        if interval[0] == [self.min,self.max]:
            interval = interval[1]
        else:
            interval = interval[0]

        # Get lists of intervals from trees
        tree1 = []
        tree2 = []
        selfIntervals = dictToInt(self.intervals)
        treeIntervals = dictToInt(tree.intervals)

        # Get all numbers that were removed
        nums = [i for i in range(interval[0],interval[1]+1) if i != 1]

        # DELETE #

        # Add all intervals that need to be removed to another list
        for i in nums:
            for j in range(len(selfIntervals)):
                if i in selfIntervals[j] and selfIntervals[j] not in tree1:
                    tree1.append(selfIntervals[j])
            for j in range(len(treeIntervals)):
                if i in treeIntervals[j] and treeIntervals[j] not in tree2:
                    tree2.append(treeIntervals[j])

        # delete all intervals from original tree
        for i in range(len(tree1)):
            selfIntervals.remove(tree1[i])
            treeIntervals.remove(tree2[i])

        # SHIFT #
        # shifting by the number of leaves we removed
        numShift = len(nums)
        for j in range(len(selfIntervals)):
            if selfIntervals[j][0]>=interval[1]:
                selfIntervals[j][0]-=numShift
            if selfIntervals[j][1]>=interval[1]:
                selfIntervals[j][1]-=numShift


            if treeIntervals[j][0]>=interval[1]:
                treeIntervals[j][0]-=numShift
            if treeIntervals[j][1]>=interval[1]:
                treeIntervals[j][1]-=numShift

        # Loop through smaller subtrees and shift
        numShift = nums[0]-1
        for j in range(len(tree1)):
            if tree1[j][0]>nums[0]:
                tree1[j][0]-=numShift
            if tree1[j][1]>nums[0]:
                tree1[j][1]-=numShift

            if tree2[j][0]>nums[0]:
                tree2[j][0]-=numShift
            if tree2[j][1]>nums[0]:
                tree2[j][1]-=numShift

        # Return a list of pairs of trees resulting from separating common edges
        return [ [OrderedTree(sorted(selfIntervals)),OrderedTree(sorted(tree1))], [OrderedTree(sorted(treeIntervals)),OrderedTree(sorted(tree2))] ]

    def getValences(self):
        """ Gets the valences of an OrderedTree object and returns it as a list """

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
    def oneOffs(self, tree):
        " " " Takes in two trees and finds the intervals that are one off and returns a dictionary. The key of the dictionary will be the type of rotation, and the value " " "
        " " " will be a list where the first element will be the interval that is added, while the second element will be the interval that is called when we rotate. " " "
        lst1 = dictToInt(self.intervals)
        lst2 = dictToInt(tree.intervals)
        common = self.commonEdges(tree)
        difference = []
        for i in lst1:##get the differences in the self tree
            if i not in common:
                difference.append(i)
        unoffs = defaultdict(list)##create a dictionary where the key is the type of rotation that is needed to undo the rotation, and the value is a list where the first index is the interval added and
        # the second index is the rotation used to add that interval
        # print(difference)
        for i in difference:
            decomp = decompassingInterval(self, i)
            encomp = encompassingInterval(self, i)
            if not decomp and encomp:##if there is no decompassing
                ##if sibling pair we can just use the rotate right and rotate left for these since the interval that is deleted is also the same as the one that is called
                unoffs["R"].append([(rotateRight(self, i))[1][1], i])# the value, aka the interval to rotate, is simply i
                unoffs["L"].append([(rotateLeft(self, i))[1][1], i])
                ##if complex subtree
            else:
                unoffs["R"].append([[decomp[0], encomp[1]], decomp])##rotating right the interval called when rotating for subtrees follow a different rule: for rotate right,
                #the added interval is min of the decompassing interval and the max of the encompassing interval, the interval to call is the decompassing interval
                unoffs["L"].append([[encomp[0], decomp[1]], decomp])##rotating left: the added interval is the min of the encompassing interval and the max of the decompassing interval
                #the interval to call is the decompassing interval

        right = []
        left = []
        for key in unoffs.keys():## delete the ones not in the lst2? or the ones in lst2? not sure brain too fried
            for added in unoffs[key]:
                # print((added))
                if list(added[0]) not in lst2:
                    # unoffs[key].remove(added)
                    if key == "R":
                        right.append(added)
                    else:
                        left.append(added)
        for delete in right:
            unoffs["R"].remove(delete)
        for delete in left:
            unoffs["L"].remove(delete)

        return unoffs

    def rotate1(self, tree):
        new_tree = copy.deepcopy(self)##make a copy to return
        rotates = oneOffs(self, tree)##get a dictonary
        for key in rotates.keys():##loop through keys: "R" or "L"
            for val in rotates[key]:##loop through the pair of values where the first is the added interval and the second is the one needed to call in rotate functions
                if key == "R":##if right rotation, make a deep copy of the rotation and set that as the original
                    new_tree = copy.deepcopy(rotateRight(new_tree, val[1])[0])
                elif key == "L":##if left rotation, make a deep copy of the rotation and set that as the original
                    new_tree = copy.deepcopy(rotateLeft(new_tree, val[1])[0])
        return [new_tree, tree]##return the two trees

    def drawPolygon(tree, **kwargs):
        """ Draws Triangulated Polygon from OrderedTree object """
        # possible attributes: placement=, color=, style=, thickness=, innerColor=, outerColor=, innerStyle=, outerStyle=, innerThickness=, outerThickness=, dottedLine=[interval,interval]
        r = lambda: random.randint(0,255)
        rand_color=('#%02X%02X%02X' % (r(),r(),r()))
        plt.axis('off')
        #default values
        innerColor=rand_color
        outerColor=rand_color
        innerStyle= '-'
        outerStyle= '-'
        innerThickness= 2
        outerThickness= 2
        placement=0
        dottedLine=0
        dottedLineColor='black'
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
        # if dottedLine is requested
        if 'dottedLine' in kwargs:
            dottedLine=1
            interval=kwargs['dottedLine']
            a=interval[0]
            b=interval[1]
        if 'dottedLineColor' in kwargs:
            dottedLineColor=kwargs['dottedLineColor']
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

        #draw dotted line
        if dottedLine==1:
            dottedLine = LineString([vertices[a-1], vertices[b]])
            plt.plot(*dottedLine.xy, linestyle=':',color=dottedLineColor)

    def drawTree(tree, **kwargs):
        """ Draws a tree from an OrderedTree object """
        # possible attributes: color=, style=, placement=, vNums=(0 or 1), scaled=(0 or 1)
        # create random default color for tree
        r = lambda: random.randint(0,255)
        rand_color=('#%02X%02X%02X' % (r(),r(),r()))
        plt.axis('off')
        #default values
        color=rand_color
        style='-'
        placement=0
        vNums=0
        scaled=0
        scale=1
        #kwargs
        if 'vNums' in kwargs:
            vNums=kwargs['vNums']
        if 'placement' in kwargs:
            placement=kwargs['placement']
        plt.rcParams["figure.figsize"] = [placement*14+11,5]
        if 'color' in kwargs:
            color=kwargs['color']
        if 'style' in kwargs:
            style=kwargs['style']
        if 'scaled' in kwargs:
            scaled=kwargs['scaled']
        n=tree.leaves
        intervals = tree.intervals
        # sets placement depending on scaled or not
        if scaled==1:
            scale=4/(n-1)
            placement = placement* (n*scale)*1.5+0.5
        else:
            placement=placement*7
        # get points for vertices of triangle
        for key,val in intervals.items():
            for i in val:
                vertices=[]
                #left coordinate
                x0=(key*scale)+ placement
                y0=0
                vertices.append((x0,y0))
                #right coordinate
                x1=(i*scale)+ placement
                y1=0
                base=x1-x0
                vertices.append((x1,y1))
                #top coordinate
                x2= (base/2)+ x0
                dist = math.sqrt( (x1 - x0)**2 + (y1 - y0)**2 )
                y2=math.sqrt((dist*dist)-((base*base)/4))
                vertices.append((x2,y2))
                #plot left & right side of triangle
                leftLine = LineString([vertices[0], vertices[2]])
                plt.plot(*leftLine.xy, color=color, linestyle=style)
                rightLine = LineString([vertices[1], vertices[2]])
                plt.plot(*rightLine.xy, color=color, linestyle=style)
                #if visible numbers is requested
                if vNums==1:
                    plt.annotate(key, (vertices[0][0], vertices[0][1] -0.01*n))
                    plt.annotate(i, (vertices[1][0], vertices[1][1]-0.01*n))

    def drawPolygonTree(tree, **kwargs):
        """ Draws a Triangulated Polygon with a tree inside, given an OrderedTree object """
        # possible attributes: placement=, color=, style=, thickness=, innerColor=, outerColor=, innerStyle=, outerStyle=, innerThickness=, outerThickness=, dottedLine=[interval,interval]
        # treeColor=, treeStyle=, treeThickness=
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
        dottedLine=0
        dottedLineColor='black'
        treeColor='red'
        treeStyle='-'
        treeThickness=1.5
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
        # if dottedLine is requested
        if 'dottedLine' in kwargs:
            dottedLine=1
            interval=kwargs['dottedLine']
            a=interval[0]
            b=interval[1]
        if 'dottedLineColor' in kwargs:
            dottedLineColor=kwargs['dottedLineColor']
        if 'treeColor' in kwargs:
            treeColor=kwargs['treeColor']
        if 'treeStyle' in kwargs:
            treeStyle=kwargs['treeStyle']
        if 'treeThickness' in kwargs:
            treeThickness=kwargs['treeThickness']

        # get points for vertices of polygon
        n=tree.leaves
        sides=tree.leaves+1
        r=3    #radius size of shape
        angle=(2*math.pi)/(sides)
        vertices=[]
        start=math.ceil(sides/2)
        offset=placement*7-7 #changes the X value of the points
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

        #create polygon using the vertices found above
        polygon1 = Polygon(vertices)
        #plot polygon
        x, y = polygon1.exterior.xy
        plt.plot(x, y, color=outerColor, linestyle=outerStyle, linewidth=outerThickness)

        # create dictionary for inner triangle vertices
        triVert=defaultdict(list)
        for i in range(n+1):
            if i+1 > n:
                triVert[i]=[i-1]
            elif i-1 < 0:
                triVert[i]=[i+1]
            else:
                triVert[i]=[i-1,i+1]

        # draw the internal edges
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
                # append the vertices to triVert dictionary
                triVert[key-1].append(i)
                triVert[i].append(key-1)

        # Create triangles out of dictionary values... Check each value at each key, and if that value as a key contains the same values, it's a triangle.
        allTriangles=[]
        lists=triVert.items()
        for key,val in triVert.items():
            for i in val:
                for j in range(len(val)):
                    element=val[j]
                    elementinlists=[element in list[1] for list in lists]
                    if elementinlists[i]==1:
                        verts=[]
                        verts.append(i)
                        verts.append(val[j])
                        verts.append(key)
                        verts.sort()
                        allTriangles.append(verts)
        allTriangles.sort()
        result = [allTriangles[i] for i in range(len(allTriangles)) if i == 0 or allTriangles[i] != allTriangles[i-1]]
        temp=[]
        # Connecting centers... the centers of two triangles will connect if they have a common edge. search through the triangle list to find triangles with a common edge, and connect their centers
        for i in range(1,len(result)):
            for triangle in result:
                a=triangle[0]
                b=triangle[1]
                c=triangle[2]
                # look for triangles w only 2 of the same points
                if a in result[i] and b in result[i] or a in result[i] and c in result[i] or b in result[i] and c in result[i]:
                    TriOne=result[i]
                    aa=TriOne[0]
                    bb=TriOne[1]
                    cc=TriOne[2]
                    triangleOne=Polygon([vertices[aa],vertices[bb],vertices[cc]])
                    triOneCenter=triangleOne.centroid
                    TriTwo=triangle
                    d=TriTwo[0]
                    e=TriTwo[1]
                    f=TriTwo[2]
                    triangleTwo=Polygon([vertices[d],vertices[e],vertices[f]])
                    triTwoCenter=triangleTwo.centroid
                    bothPts=[triOneCenter.x, triOneCenter.y,triTwoCenter.x, triTwoCenter.y]
                    bothPts.sort()
                    # Only draw a line if it has not been drawn yet. Append each line into temp list to store all the lines that have been made
                    if bothPts not in temp:
                        internalConnectingLine = LineString([triOneCenter, triTwoCenter])
                        plt.plot(*internalConnectingLine.xy, color=treeColor,linestyle=treeStyle, linewidth=treeThickness)
                        temp.append(bothPts)
                        temp.sort()
        # Find the outer triangles and draw the external lines
        for triangle in result:
            a=triangle[0]
            b=triangle[1]
            c=triangle[2]
            # Look for the triangles with two external lines leaving the polygon... aka vertices are all next to each other
            if b+1==c and b-1==a or a==0 and b==1 and c==n or a==0 and b==n-1 and c==n:
                midpointOneX=(vertices[a][0]+vertices[b][0])/2
                midpointOneY=(vertices[a][1]+vertices[b][1])/2
                midpointTwoX=(vertices[b][0]+vertices[c][0])/2
                midpointTwoY=(vertices[b][1]+vertices[c][1])/2
                if a==0 and b==1 and c==n:
                    midpointTwoX=(vertices[a][0]+vertices[c][0])/2
                    midpointTwoY=(vertices[a][1]+vertices[c][1])/2
                if a==0 and b==n-1 and c==n:
                    midpointOneX=(vertices[b][0]+vertices[c][0])/2
                    midpointOneY=(vertices[b][1]+vertices[c][1])/2
                    midpointTwoX=(vertices[a][0]+vertices[c][0])/2
                    midpointTwoY=(vertices[a][1]+vertices[c][1])/2
                midpointOne=(midpointOneX,midpointOneY)
                midpointTwo=(midpointTwoX,midpointTwoY)
                outerTriangle=Polygon([vertices[a],vertices[b],vertices[c]])
                outerTriangleCenter=outerTriangle.centroid

                distance1=math.sqrt((outerTriangleCenter.x-midpointOneX)**2 + (outerTriangleCenter.y-midpointOneY)**2)
                newX1=midpointOneX + (midpointOneX - outerTriangleCenter.x) / distance1 * 0.5
                newY1=midpointOneY + (midpointOneY - outerTriangleCenter.y) / distance1 * 0.5
                newPoint=(newX1, newY1)
                tailOne = LineString([outerTriangleCenter, newPoint])
                plt.plot(*tailOne.xy, color=treeColor,linestyle=treeStyle, linewidth=treeThickness)

                distance2=math.sqrt((outerTriangleCenter.x-midpointTwoX)**2 + (outerTriangleCenter.y-midpointTwoY)**2)
                newX2=midpointTwoX + (midpointTwoX - outerTriangleCenter.x) / distance2 * 0.5
                newY2=midpointTwoY + (midpointTwoY - outerTriangleCenter.y) / distance2 * 0.5
                newPoint2=(newX2, newY2)
                tailTwo = LineString([outerTriangleCenter, newPoint2])
                plt.plot(*tailTwo.xy, color=treeColor,linestyle=treeStyle, linewidth=treeThickness)
            # triangles with only 1 external line... if two vertices are next to each other, and the third is elsewhere
            elif b+1==c and a+1!=b or a+1==b and b+1!=c or a==0 and c==n:
                midpointX=(vertices[b][0]+vertices[c][0])/2
                midpointY=(vertices[b][1]+vertices[c][1])/2
                if a+1==b and b+1!=c:
                    midpointX=(vertices[a][0]+vertices[b][0])/2
                    midpointY=(vertices[a][1]+vertices[b][1])/2
                if a==0 and c==n:
                    midpointX=(vertices[a][0]+vertices[c][0])/2
                    midpointY=(vertices[a][1]+vertices[c][1])/2
                midpoint=(midpointX,midpointY)
                outerTriangle=Polygon([vertices[a],vertices[b],vertices[c]])
                outerTriangleCenter=outerTriangle.centroid
                distance=math.sqrt((outerTriangleCenter.x-midpointX)**2 + (outerTriangleCenter.y-midpointY)**2)
                newX1=midpointX + (midpointX - outerTriangleCenter.x) / distance * 0.5
                newY1=midpointY + (midpointY - outerTriangleCenter.y) / distance * 0.5
                newPoint=(newX1, newY1)
                tail=LineString([outerTriangleCenter, newPoint])
                plt.plot(*tail.xy, color=treeColor,linestyle=treeStyle, linewidth=treeThickness)

        #draw dotted line
        if dottedLine==1:
            dottedLine = LineString([vertices[a-1], vertices[b]])
            plt.plot(*dottedLine.xy, linestyle=':',color=dottedLineColor)
        plt.axis('off')

def isOrdered(newick):
    """ Checks if a tree is ordered """
    newickTuple = ""
    # Can't edit a tuple
    for i in newick:
        if i == "(":
            newickTuple+="["
        elif i == ")":
            newickTuple+="]"
        else:
            newickTuple+=i

    newickTuple = eval(newickTuple)
    orderNewick(newickTuple)
    newickTuple = str(tuple(newickTuple))
    num = 0

    # Check for order
    for i in newickTuple:
        if i.isnumeric() and int(i) == num+1:
            num = int(i)
        elif i.isnumeric() and int(i) != num+1:
            return None

    # return tree
    return newickTuple.replace(" ","")


def orderNewick(newick):
    """ Helper Function for isOrdered that will try to order a tree """

    # Base Case
    if isinstance(newick, int):
        return newick

    # Recursive step
    left = orderNewick(newick[0])
    right = orderNewick(newick[1])

    # Get max of tuple
    if not isinstance(left, int):
        left = left[1]

    if not isinstance(right, int):
        right = right[1]

    # Compare and swap
    if left > right:
        max = left
        temp = newick[1]
        newick[1] = newick[0]
        newick[0] = temp
    else:
        max = right

    # Turn into tuple
    if not isinstance(newick[1], int):
        newick[1] = tuple(newick[1])
    if not isinstance(newick[0], int):
        newick[0] = tuple(newick[0])


    return max

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
        return [OrderedTree(), OrderedTree()]

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

    return [OrderedTree(selfIntervals), OrderedTree(treeIntervals)]

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


def decompassingInterval(self, interval):
    """ Given an OrderedTree object and an interval, return the largest interval inside the input interval. """
    ##two cases, either decompassing will share a key or a value
    ##if key:
    for val in self.intervals.get(interval[0]):##loop through values in the key
        if val < interval[1]:## if value is less than the input value, we return that as the decompassingInterval
            return [interval[0], val]
    ##if they share a value:
    ##loop through keys and find which key greater than interval[0] has the value interval[1]
    for key in self.intervals.keys():
        if key > interval[0]:
            if interval[1] in self.intervals[key]:
                return [key,interval[1]]
    return None

#Encompassing Interval Method:
def encompassingInterval(ordTree, interval):
  """ Given an OrderedTree object and an interval, return the smallest interval encasing input interval. """
  tree = ordTree.intervals
  inKey = interval[0]
  inVal = interval[1]

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


def rotateRight(tree1, interval):
    """ Given a tree and interval, rotate interval to a right subtree if possible. """
    #if interval max is not a value in key (it is a min so can't rotate right)
    tree = copy.deepcopy(tree1)
    changed_intervals = []
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
    if(lonepair):#if its a sibling pair, or lonepair
        if(encomp[1] == interval[1]):#make sure if can't rotate
            return None
        #if interval is lone pair
        if(encomp[0] == interval[0]):#if original interval and encompassing interval share a min
            changed_intervals.append([interval[0], interval[1]])
            tree.intervals[interval[0]].remove(interval[1])#remove the max from the key
            if(not tree.intervals[interval[0]]):#if the key is now empty not sure if this is necessary
                del tree.intervals[interval[0]]#delete the key
            tree.intervals.setdefault(interval[1],[encomp[1]])#create a new key with the given interval max and set its value to the encompassing max
            changed_intervals.append([interval[1],encomp[1]])
            tree.intervals = OrderedDict(sorted(tree.intervals.items()))#sort
        return tree, changed_intervals

    #if lonepair is FALSE
    if(interval[0] == encomp[0]):#if min of given interval is the same as min of encompassing, you cannot rotate right
        return None
    elif(interval[1] == tree.max):#if the max of interval is the largest leaf
        return None
    elif(interval[0] == tree.min):#if the min of the interval is the smallest leaf
        return None
    elif(interval[1] == interval[0]):#if the interval min == interval max ie: [2,2]
        return None
    try:
        tree.intervals[encomp[0]].remove(encomp[1])#remove the encompassing interval
    except:
        return None
    changed_intervals.append([encomp[0], encomp[1]])
    if(not (tree.intervals[encomp[0]])):#if its empty, delete the key, not sure if needed
        del tree.intervals[encomp[0]]
    #loop through key of encompassing intervals
    for val in tree.intervals[encomp[0]]:
        if val > interval[1]:
            tree.intervals[interval[0]].append(val)
            changed_intervals.append([interval[0], val])
            tree.intervals[interval[0]] = sorted(tree.intervals[interval[0]])
            return tree, changed_intervals

    return None

def rotateLeft(tree1, interval):
    """ Given a tree and interval, rotate interval to a left subtree if possible. """
    tree = copy.deepcopy(tree1)
    changed_intervals = []
    #if interval max is not a value in key (it is a min so can't rotate right)
    if(interval[1] not in tree.intervals[interval[0]]):#if the input interval doesnt consist of a real [min max]
        return None

    lonepair = False

    #check if interval max is a lone pair or not
    if len(tree.intervals[interval[0]]) == 1:
        lonepair = True

    encomp = encompassingInterval(tree, interval)#get encompassing interval

    #if lonepair is TRUE
    if(lonepair):
        if(encomp[0] == interval[0]):#make sure if can't rotate
            return None
        #if interval is lone pair , rotate left
        if(encomp[1] == interval[1]):#if original interval and encompassing interval share a min
            changed_intervals.append([interval[0], tree.intervals[interval[0]][0]])
            del tree.intervals[interval[0]]#delete the key
            tree.intervals[encomp[0]].append(interval[0])
            changed_intervals.append([encomp[0],interval[0]])
            tree.intervals[encomp[0]] = sorted(tree.intervals[encomp[0]])#sort
        return tree, changed_intervals

    #if lonepair is FALSE
    if(interval[1] == encomp[1]):#if min of given interval is the same as min of encompassing, you cannot rotate right
        return None
    elif(interval[1] == tree.max):#if the max of interval is the largest leaf
        return None
    elif(interval[0] == tree.min):#if the min of the interval is the smallest leaf
        return None
    elif(interval[1] == interval[0]):#if the interval min == interval max ie: [2,2]
        return None
    changed_intervals.append([interval[0], encomp[1]])
    try:
        tree.intervals[interval[0]].remove(encomp[1])#remove the encompassing interval
    except:
        return None
    lst = list(tree.intervals.keys())
    lst = sorted(lst)
    for i in range(len(lst)-1, -1, -1):#find the next smallest key behind interval[0] to attach
        if lst[i] < interval[0] and tree.intervals[lst[i]].count(encomp[1]):
            tree.intervals[lst[i]].append(interval[1])
            changed_intervals.append([lst[i], interval[1]])
            tree.intervals[lst[i]] = sorted(tree.intervals[lst[i]])
            return tree, changed_intervals
    return None

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
