"""
First Draft:  Cut and paste all the different versions.  Need to merge into a single class, and fix typos and indentation
"""


Class OrderedTree:
  def __init__(self, n: int):
  “ “ “ Takes an Int and creates a dictionary with intervals [1,2]...[1,n] “ “ “
		Self.intervals = defaultdict(list)
    Self.leaves = n
    For i in range(2,n+1):
      self.tree[1].append(i)

	def __init__(self, interval):
“ “ “ Takes in list, or string that converts to list, and creates a dictionary from it “ “ “
		If isInstance(interval, string):
			Interval = ‘[‘ + interval + ‘]’
			Interval = eval(interval)
		Self.intervals = defaultdict(list)
		Leaf = set()
For i in interval:
	self.intervals[i[0]].append(i[1])
	leaf.add(i[0])
	leaf.add(i[1])
Self.leaves = len(leaf)


def __str__(self):
“ “ “ Prints dictionary in interval format “ “ “
	result = ‘’
	For key, val in self.interval.items():
		for i in val:
			result += “[“+key+ “,”+i+ “],”
	return result[:-1]

def __eq__(self, otherTree):
“ “ “ Returns true if two trees are the same and false otherwise “ “ “
	If self.interval.leaves
If (self.interval.keys() != otherTree.interval.keys()):
	return False
for key in self.interval.keys():
	If self.interval[key] != otherTree.interval[key]:
		return False
return True

from collections import defaultdict

class orderedTree:
	def __init__(self, n: int):
	“ “ “ Creates a caterpillar tree with the inputted int ” “ “
		self.tree = defaultdict(list)
		self.leaves = n
		for i in range(2,n+1):
			self.tree[1].append(i)
	def __init__(self, n:str): #needs newick2interval()
	“ “ “ Creates a tree based on a string inputted in newick notation “ “ “
		for c in n:
			if(c.isnumeric()):
				++self.leaves
		self.tree = defaultdict(list)

	def __init__(self, n: list):
	“ “ “ Creates a tree based on a list entered in intervals (List of lists) “ “ “
		self.tree = defaultdict
		for k, v in n:
			self.tree[k].append(v)

	def __str__(self):
	“ “ “ Allows for printing of dictionary and # of leaves“ “ “
		lst = list(zip(self.tree.keys(), self.tree.values()))
		return(f"(Dictionary: {lst}\n# of leaves = {self.leaves}")

	def __eq__(self, tree):
	“ “ “Allows for == override “ “ “
		if(list(self.tree.items()) == (list(tree.tree.items()))):
			return True
		return False

from collections import defaultdict

class orderedTree:
    
    
    d = defaultdict(int)
    
    # default constructor that takes in positive number n
    # [ [1,2],[1,3],[1,4]...[1,n] ]
    # Example: [ [1,2], [1,3], [1,4], [1,5], [1,6]]
    def __init__(self, n, intervals):
        s = []

        left = 1
        right = 2
        
        for a in range(2, n+1):
            row = []
            for b in range(1):
                row.append(left)
                row.append(right)
                right+= 1
                    
            s.append(row)
​
        
        # list to dictionary
        # [ [1,2], [1,3], [1,4], [1,5], [1,6]]
        # d{1:[2,3,4,5,6]}
​
        
    
        #converts list to string
        list_to_string = ' '.join(str(c) for c in s)
        print(list_to_string)
        
        self.interval = s
        
    #print out interval
    def __str__(self):
        print(self.interval)
    
    
        
    #print out interval
    #def print_interval(self):
        #print(self.interval)
        
    #Interval to Newick
    # [1,2],[1,3],[1,4]...[1,n]
    # (1,2),3),4),...n)
    def int_to_newick(self, interval):
        pass
        
    #def __bool__(self,tree1, tree2):
    #   return False

a = orderedTree(5)
a.__str__()
#a.print_interval()

# [1,2],[1,3],[1,4]...[1,n]

#should return newick
#int_to_newick([1,2],[1,3],[1,4])

tree1 = [1,2],[1,3],[1,4]
tree2 = [1,3],[1,4],[1,5]

#__bool__(tree1,tree2)
