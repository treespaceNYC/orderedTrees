from orderedTree import OrderedTree, decompassingInterval, dictToInt
from collections import OrderedDict
import numpy as np
import heapq

def dictToHeap(intervals):
    intervals = dictToInt(intervals)
    h = []
    heapq.heapify(h)

    for i in intervals:
        t = (i[1] - i[0], i)
        heapq.heappush(h,t)

    return h

class TreeHelper:
    def __init__(self, tree1, tree2):
        self.table_ = np.ones((tree1.leaves, tree2.leaves), dtype = int) *-1
        self.xHash_ = OrderedDict()
        self.yHash_ = OrderedDict()


        #fills hashes up with leaves
        index = 0
        for i in range(tree1.min, tree1.max+1):
            self.xHash_[index] = (i,i)
            index+=1

        h = dictToHeap(tree1.intervals)
        while(h):
            self.xHash_[index] = tuple(heapq.heappop(h)[1])
            index+=1


        index = 0
        for i in range(tree2.min, tree2.max+1):
            self.yHash_[index] = (i,i)
            index+=1

        h = dictToHeap(tree2.intervals)
        while(h):
            self.yHash_[index] = tuple(heapq.heappop(h)[1])
            index+=1

    def mast(self, leftTree: OrderedTree, rightTree: OrderedTree):
        
        decomp = {}
        for i in range(len(self.table)):
            d = decompassingInterval(leftTree,self.yHash_[i])
            for j in range(len(self.table[i])):

                # if self.__collides__():
                #     if (self.yHash_[i][0] == self.yHash_[i][1]) or (self.xHash_[i][0] == self.xHash_[i][1]):
                #         self.table[i][j] = 1



                decomp[self.table[j]] = decompassingInterval(leftTree,self.xHash_[j])