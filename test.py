from temp import *

### create two trees to compare
tree1 = randOrdered(100)
tree2 = randOrdered(100)


### create treehelper object to calculate MAST
helper = TreeHelper(tree1, tree2)

### get mast number from trees used to initialize helper ->int
MAST_NUM = helper.mast()

### get MAST tree from trees used to initialize helper ->OrderedTree

MAST_TREE = helper.getMastTree()


### drawing trees for visualization 
tree1.drawTree(vNums = 1)
tree2.drawTree(placement = 2, vNums = 1)
MAST_TREE.drawTree(placement = 3, vNums = 1)

plt.show()


tree1.drawPolygon(placement = 1)
tree2.drawPolygon(placement = 2)
MAST_TREE.drawPolygon(placement = 3)

plt.show()
