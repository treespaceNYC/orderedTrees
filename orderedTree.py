"""
First Draft:  Cut and paste all the different versions.  Need to merge into a single class, and fix typos and indentation
"""
from collections import defaultdict


class orderedTree:
"""
First Draft:  Cut and paste all the different versions.  Need to merge into a single class, and fix typos and indentation
"""
from collections import defaultdict


class orderedTree:
    def __init__(self, n: int):
        " " "Takes an Int and creates a dictionary with intervals[1, 2]...[1, n]" " "
        self.intervals = defaultdict(list)
        self.leaves = n
        for i in range(2,n+1):
            self.intervals[1].append(i)

    def __init__(self, n: list):
        " " " Creates a tree based on a list entered in intervals (List of lists) " " "
        self.intervals = defaultdict(list)
        for k, v in n:
            self.intervals[k].append(v)
        self.leaves = len(self.intervals.keys()) + len(self.intervals.values())



    def __str__(self):
        " " "Allows for printing of dictionary and # of leaves " " "
        lst = list(zip(self.intervals.keys(), self.intervals.values()))
        return(f"(Dictionary: {lst}\n# of leaves = {self.leaves}")


    def __eq__(self, tree):
        " " "Allows for == override " " "
        if(list(self.tree.items()) == (list(tree.tree.items()))):
            return True
        return False


# test = orderedTree(3)
# test1 = orderedTree([[1,3], [1,4], [2,3]])
# print(test)
# print(test1)
