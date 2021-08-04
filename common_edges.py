from collections import OrderedDict, defaultdict

#Need to include a way for python to know which constructor to use.

class OrderedTree:
    def __init__(self, *n):
            self.leaves = 0
            self.intervals = defaultdict(list)
            if(len(n) == 0):
                """ Default constructor that creates an empty tree """
                self.leaves = 0
            # print(n)
            if(isinstance(n[0], int)):
                """ Takes an Int and creates a dictionary with intervals[1, 2]...[1, n] """
                self.leaves = n[0]
                for i in range(2,n[0]+1):
                    self.intervals[1].append(i)
            elif(isinstance(n[0], list)):
                """ Creates a tree based on a list entered in intervals (List of lists) """
                max = 0
                for k, v in n[0]:
                    self.intervals[k].append(v)
                    if(v > max):
                        max = v
                    if(k > max):
                        max = k
                self.leaves = max


    def __str__(self):
        """ Allows for printing of dictionary and # of leaves """
        lst = list(zip(self.intervals.keys(), self.intervals.values()))
        return(f"(Dictionary: {lst}\n# of leaves = {self.leaves}")


    def __eq__(self, tree):
        """ Allows for == override """
        if(list(self.intervals.items()) == (list(tree.intervals.items()))):
            return True
        return False

    def commonEdges(self, tree1):
        lst = []
        for key in tree1.intervals.keys():
            if(key in self.intervals.keys()):
                for i in tree1.intervals.get(key):
                    for j in self.intervals.get(key):
                        if(i == j):
                            lst.append([key, i])
                            break
        return lst
