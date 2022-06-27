from orderedTree import OrderedTree, decompassingInterval, dictToInt
from collections import OrderedDict
import numpy as np
import heapq

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
        self.xHash_ = OrderedDict()
        self.yHash_ = OrderedDict()

        self.xIndex_ = OrderedDict()
        self.yIndex_ = OrderedDict()


        #fills hashes up with leaves
        index = 0
        for i in range(tree2.min, tree2.max+1):
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
        for i in range(tree1.min, tree1.max+1):
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



    def mast(self, leftTree: OrderedTree, rightTree: OrderedTree):
        """Takes in two trees and returns a table with the corresponding mast for each leaf and interval

        Parameters:
            leftTree: OrderedTree
            rightTreeL OrderedTree
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
                c = self.__collides__(self.yHash_[i],self.xHash_[j])
                if c <= 2: # edge case
                    self.table_[i][j] = c

                # larger case where lookup table is needed to compute mast
                else:
                    l1 = d[0]                        # y - left child
                    l2 = decomp[self.xHash_[j]][0]   # x - left child

                    r1 = d[1]                        # y - right child
                    r2 = decomp[self.xHash_[j]][1]   # x - right child

                    # BIG FORMULA - ll + rr, lr + rl, al, la, ar, ra
                    self.table_[i][j] = max(
                        self.table_[ self.yIndex_[tuple(l1)] ][ self.xIndex_[tuple(l2)] ] + self.table_[ self.yIndex_[tuple(r1)] ][ self.xIndex_[tuple(r2)] ],
                        self.table_[ self.yIndex_[tuple(l1)] ][ self.xIndex_[tuple(r2)] ] + self.table_[ self.yIndex_[tuple(r1)] ][ self.xIndex_[tuple(l2)] ],
                        self.table_[i][ self.xIndex_[tuple(l2)] ],
                        self.table_[i][ self.xIndex_[tuple(r2)] ],
                        self.table_[ self.yIndex_[tuple(l1)] ][j],
                        self.table_[ self.yIndex_[tuple(r1)] ][j]
                    )
        return self.table_
