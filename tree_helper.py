from orderedTree import *
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
        count = 0
        for i in range(tree1.min, tree1.max+1):
            self.xHash_[(i,i)] = count
            count+=1

        h = dictToHeap(tree1.intervals)
        while(h):
            self.xHash_[tuple(heapq.heappop(h)[1])] = count
            count+=1


        count = 0
        for i in range(tree2.min, tree2.max+1):
            self.yHash_[(i,i)] = count
            count+=1

        h = dictToHeap(tree2.intervals)
        while(h):
            self.yHash_[tuple(heapq.heappop(h)[1])] = count
            count+=1


# # tree1 = OrderedTree(10)
# tree1 = randOrdered(10)

# meep = dictToHeap(tree1.intervals)
# # print(len(meep))
# # while(meep):
# #     print(heapq.heappop(meep))
# tree2 = OrderedTree(10,-1)
# #
# SOS = TreeHelper(tree1,tree2)
# #
# #
# print(SOS.table_)
# print(SOS.xHash_)
# print(SOS.yHash_)
