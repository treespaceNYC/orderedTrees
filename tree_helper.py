from orderedTree import OrderedTree, decompassingInterval, dictToInt
from collections import OrderedDict
import numpy as np
import heapq
import copy

def dictToHeap(intervals):
    """Takes in intervals in the form of a dictionary and returns a min heap
    where the priority is the distance between two intervals and the item is the interval itself

    Parameters:
        intervals: a dictionary of our intervals
    Returns:
        A heap where the priority is the distance between two intervals and the item is the interval itself
    """
    intervals = dictToInt(intervals) ## could be optimized
    h = []
    heapq.heapify(h)

    for i in intervals:
        t = (i[1] - i[0], i)
        heapq.heappush(h,t)

    return h

class TreeHelper:
    def __init__(self, tree1, tree2):
        self.table_ = np.ones((2*tree1.leaves - 1, 2*tree2.leaves - 1), dtype = int) *-1

        # self.table_ = [([-1]*(2*tree1.leaves - 1))]
        self.table_ = [[[-1,[]] for i in range(2*tree1.leaves - 1)] for i in range(2*tree1.leaves - 1)]


        self.xHash_ = OrderedDict()
        self.yHash_ = OrderedDict()

        self.xIndex_ = OrderedDict()
        self.yIndex_ = OrderedDict()


        #fills hashes up with leaves
        index = 0
        for i in tree2.edges:
            self.xHash_[index] = (i,i)
            self.xIndex_[(i,i)] = index
            index+=1

        h = dictToHeap(tree2.intervals)
        while(h):
            val = tuple(heapq.heappop(h)[1])
            self.xHash_[index] = val
            self.xIndex_[val] = index
            index+=1


        index = 0
        for i in tree1.edges:
            self.yHash_[index] = (i,i)
            self.yIndex_[(i,i)] = index
            index+=1

        h = dictToHeap(tree1.intervals)
        while(h):
            val = tuple(heapq.heappop(h)[1])
            self.yHash_[index] = val
            self.yIndex_[val] = index
            index+=1

    def __collides__(self, left, right):
        """Takes in two intervals and returns the number of overlap between the them

        Parameters:
            left: interval ex: [1,2]
            right: interval ex: [3,4]
        Returns:
            returns an integer for the overlap
        """
        # if left interval is a leaf and is in the right interval
        if(left[0] == left[1]) and ((left[0] >= right[0]) and (left[0] <= right[0])):
            return 1

        # if right interval is a leaf and is in the left interval
        if(right[0] == right[1]) and ((right[0] >= left[0]) and (right[0] <= left[0])):
            return 1

        #return the overlap
        return max(0, min(left[1], right[1]) - max(left[0], right[0])+1)



    def __build__(self, leftTree: OrderedTree, rightTree: OrderedTree):
        """Takes in two trees and returns a table with the corresponding mast for each leaf and interval

        Parameters:
            leftTree: OrderedTree
            rightTree: OrderedTree
        Returns:
            returns a table with the corresponding mast for each leaf and interval
        """

        decomp = {}
        for i in range(len(self.table_)):

            # get children for left tree
            d = decompassingInterval(leftTree,self.yHash_[i])

            # loop through nxn array
            for j in range(len(self.table_[i])):

                # store children for right tree in a lookup table to decrease compute time
                if(self.xHash_[j] not in decomp.keys()):
                    decomp[self.xHash_[j]] = decompassingInterval(rightTree,self.xHash_[j])

                # check how many times two intervals collide
                if self.yHash_[i][0] == self.yHash_[i][1] or self.xHash_[j][0] == self.xHash_[j][1]: # edge case
                    c = self.__collides__(self.yHash_[i],self.xHash_[j])
                    self.table_[i][j][0] = c
                    self.table_[i][j][1] = [[[self.yHash_[i],self.xHash_[j]]]]

                # larger case where lookup table is needed to compute mast
                else:
                    l1 = tuple(d[0])                        # y - left child
                    l2 = tuple(decomp[self.xHash_[j]][0])   # x - left child

                    r1 = tuple(d[1])                        # y - right child
                    r2 = tuple(decomp[self.xHash_[j]][1])   # x - right child

                    # BIG FORMULA - ll + rr, lr + rl, al, la, ar, ra
                    temp = (
                        [self.table_[ self.yIndex_[l1] ][ self.xIndex_[l2] ][0] + self.table_[ self.yIndex_[r1] ][ self.xIndex_[r2] ][0],[[l1,l2],[r1,r2]]],
                        [self.table_[ self.yIndex_[l1] ][ self.xIndex_[r2] ][0] + self.table_[ self.yIndex_[r1] ][ self.xIndex_[l2] ][0],[[l1,r2],[r1,l2]]],
                        [self.table_[i][ self.xIndex_[l2] ][0],[[self.yHash_[i],l2]]],
                        [self.table_[i][ self.xIndex_[r2] ][0],[[self.yHash_[i],r2]]],
                        [self.table_[ self.yIndex_[l1] ][j][0],[[l1,self.xHash_[j]]]],
                        [self.table_[ self.yIndex_[r1] ][j][0],[[r1,self.xHash_[j]]]]
                    )

                    m = max(temp)[0]
                    for l in temp:
                        if l[0] == m:
                            # print(m,l)
                            self.table_[i][j][0] = m
                            self.table_[i][j][1].append(l[1])

    def mast(self, leftTree: OrderedTree, rightTree: OrderedTree):
        lMast = []
        rMast = []
        self.__build__(leftTree, rightTree)
        stack = []
        stack.append([[self.yHash_[len(self.table_)-1], self.xHash_[len(self.table_)-1]]])
        while(stack):
            currIntervals = stack.pop()
            for i in currIntervals:
                # print(i)
                if( self.table_[self.yIndex_[i[0]]][self.xIndex_[i[1]]][0] != 0):
                    if(i[0][0] == i[0][1]):
                        lMast.append(i[0][0])
                    if(i[1][0] == i[1][1]):
                        rMast.append(i[1][1])
                    if(i[1][0] != i[1][1] and i[0][0] != i[0][1]):
                        stack.append(self.table_[self.yIndex_[i[0]]][self.xIndex_[i[1]]][1][0])
            # print(self.table_[self.yIndex_[i[0]]][self.xIndex_[i[1]]])
        return set(lMast + rMast)


    def getMastTree(self, leftTree: OrderedTree, rightTree: OrderedTree):
        res = copy.deepcopy(leftTree)
        leaves = self.mast(leftTree, rightTree)
        max = leftTree.max+1
        for i in range(1, max):
            if i not in leaves:
                res = res.deleteLeaf(i)

        return res
