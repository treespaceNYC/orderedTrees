from collections import defaultdict
#Need to include a way for python to know which constructor to use.

class orderedTree:
    def __init__(self, *n):
        if(len(n) == 0):
            """ Default constructor that creates an empty tree """
            self.leaves = 0
            self.tree = defaultdict(list)

        elif(isinstance(n, int)):
            """ Takes an Int and creates a dictionary with intervals[1, 2]...[1, n] """
            self.intervals = defaultdict(list)
            self.leaves = n
            for i in range(2,n+1):
                self.intervals[1].append(i)

        elif(isinstance(n, list)):
            """ Creates a tree based on a list entered in intervals (List of lists) """
            self.intervals = defaultdict(list)
            max = 0
            for k, v in n:
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

