"""
First Draft:  Cut and paste all the different versions.  Need to merge into a single class, and fix typos and indentation
"""
from collections import defaultdict


class orderedTree:
  def __init__(self, n: int):
  “ “ “ Takes an Int and creates a dictionary with intervals[1, 2]...[1, n] “ “ “
		self.intervals = defaultdict(list)
    self.leaves = n
    for i in range(2,n+1):
      self.tree[1].append(i)

	def __init__(self, interval):
“ “ “ Takes in list, or string that converts to list, and creates a dictionary from it “ “ “
		if isInstance(interval, string):
			interval = ‘[‘ + interval + ‘]’
			interval = eval(interval)
		self.intervals = defaultdict(list)
		leaf = set()
        for i in interval:
        	self.intervals[i[0]].append(i[1])
        	leaf.add(i[0])
        	leaf.add(i[1])
        self.leaves = len(leaf)
        # other versions
        #	“ “ “ Creates a tree based on a list entered in intervals (List of lists) “ “ “
        #		self.tree = defaultdict
        #		for k, v in n:
        #			self.tree[k].append(v)



def __str__(self):
“ “ “ Allows for printing of dictionary and # of leaves“ “ “
    lst = list(zip(self.tree.keys(), self.tree.values()))
    return(f"(Dictionary: {lst}\n# of leaves = {self.leaves}")

def __eq__(self, otherTree):
“ “ “ Returns true if two trees are the same and false otherwise “ “ “
	if self.interval.leaves
    if (self.interval.keys() != otherTree.interval.keys()):
        return False
    for key in self.interval.keys():
	       if self.interval[key] != otherTree.interval[key]:
               return False
    return True

#	def __eq__(self, tree):
#	“ “ “Allows for == override “ “ “
#		if(list(self.tree.items()) == (list(tree.tree.items()))):
#			return True
#		return False
