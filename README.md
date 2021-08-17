# OrderedTrees

Code for storing and comparing ordered trees.

Stores a tree in dictionary format using defaultdict from collections.
- Dictionary has left intervals as the keys and right intervals in a list for each key.

Overrides print function to print the stored tree and number of leaves.

Overrides equals operator in order to allow for comparison of two trees.

## Contributors

- [Adrian Mok](https://adrian-mok15.github.io/) - [Adrian-Mok15](https://github.com/Adrian-Mok15)
- [Amy Tse](https://amy-tse.github.io/) - [amy-tse](https://github.com/amy-tse)
- [Daniel Elkik](https://delkik.github.io/) - [Delkik](https://github.com/Delkik)
- [Diana Luna](https://dianaluna0201.wixsite.com/my-site) - [dianaluna01](https://github.com/dianaluna01)
- [Joyce Zhang](https://jzblank.github.io/) - [JZBlank](https://github.com/JZBlank)
- [Katherine St. John](https:://stjohn.github.io/) - [stjohn](https://github.com/stjohn)
- [Steven Salto](https://stevensalto.github.io/) - [StevenSalto](https://github.com/StevenSalto)



## Dependencies
- Python 3.9.x
- Shapely
  - `pip install Shapely`
- Matplotlib
  - `pip install -U matplotlib`

## Installation
Download orderedTree.py and place it in your working directory

## Examples

### Preprocessing
The orderedTree.py file allows the user to convert their tree into various notations. This includes:
- Python Dictionary
  - The keys are the minimum intervals and the values are the lists of their maximum intervals 
- List of Intervals
- Newick notation as a string

There are various functions to convert these notations between themselves.
- `dictToInt(dictionary)` will convert a tree in dictionary format
  - `dictToInt({1:[2,3,4,5]})` will return [[1,2],[1,3],[1,4],[1,5]]
- `newick2interval(string)` will convert a string in newick format to a list of intervals
  - `newick2interval("((((1,2),3),4),5)")` will return [[1,2],[1,3],[1,4],[1,5]]
- `interval2newick([[1,2],[1,3],[1,4],[1,5]])` will return `"((((1,2),3),4),5)"`

In order to check if a string in newick notation is ordered, the function `isOrdered(string)` can be used.\
`isOrdered(string)` will return the string in ordered format if its possible which will act as a True value. If it is impossible to order, it will return None.

### Building Trees
The OrderedTree constructor accepts multiple input types:
- No input for an empty constructor, produces a tree with no leaves.
  - `tree = OrderedTree()`
- An Int, n, that creates a caterpillar tree with n leaves
  - `tree = OrderedTree(4)`
- A List of Intervals
  - `tree = OrderedTree([[1,2],[1,4],[3,4]])`
- A String in Newick notation
  - `tree = OrderedTree("(((1,2),3),4)")`

It's also possible to create both random intervals and random OrderedTree objects. 
- `randInterval()` will create random Intervals based on the input. If impossible, the function will return `None`. The function takes in two or one arguments. 
`randInterval(1,5)` will create random intervals based on these two ints. `randInterval([1,5])` will do the same.
  - `randInterval(1,4)` may result in [[1,2],[3,4]] or [[1,3]] or [[3,4]]

- `randOrdered(n)` will create a random OrderedTree object with n leaves.
  - `randOrdered(20)` may create a tree with intervals: \
[1,2], [1,3], [1,14], [1,20], [4,5], [4,8], [4,9], [4,14], [6,8], [7,8], [10,14], [10,11], [12,14], [13,14], [15,16], [15, 18], [15,20], [17,18], [19,20] 
<p align=center>
  <img src="https://i.imgur.com/xibxwHM.png" height="300">
</p>

### Rotating Trees
In order to rotate intervals in a tree, the user has the option of `rotateRight(tree,interval)` and `rotateLeft(tree,interval)`
- `rotateRight(tree,interval)` will try to rotate the interval right. If successful then it will return a tuple containing the rotated OrderedTree and a list of the rotated intervals, otherwise it will return `None`.
  ```
  tree = OrderedTree([[1,7], [2,6], [2,7], [3,5], [3,6], [4,5]])
  newTree = rotateRight(tree, [3,6])[0]tree = OrderedTree([[1,7], [2,6], [2,7], [3,5], [3,6], [4,5]])
  deletedInterval = rotateRight(tree, [3,6])[1][0]
  addedInterval = rotateRight(tree, [3,6])[1][1]
  ```
  <p align="center">
    <img src="https://i.imgur.com/0RkeaFH.png" height="300" >
  </p>

### Drawing Trees
`drawTree(tree, **kwargs)` is the function used to draw trees when given an OrderedTree object. It allows the user to change the design and placement of the tree. Possible keyword arguments include:
- color= ('color' or 'hexcode')
  - If no color is specified, a random color will be chosen
- style= ('', ' ', 'None', '--', '-.', '-', ':')
  - If no style is specified, a solid line will be drawn
- placement= 
  - If no placement is specified, tree is drawn in placement 0
  - `placement = 1` will print the second tree to the right side of the first tree
  - to draw overlapping trees, allocate 0.03 between placements. ex: `placement = 0` and `placement = 0.03` draws overlapping trees
- vNums=(0 or 1)
  - If not specified, an unnumbered tree will be drawn
  - `vNums = 1` marks the tree with numbers at the bottom of each leaf
- scaled=(0 or 1)
  - When comparing trees with differing number of leaves, use `scale = 1` for the drawings to have the same height

<b>Example: Drawing Two Trees<b>
  ```
  tree = OrderedTree([[1,2], [1,5], [1,8], [3,4], [3,5], [6,7], [6,8]])
  test1 = OrderedTree([[1,8], [1,2], [3,8], [3,7], [3,6], [4,6], [5,6]])
  test1.drawTree(color='blue', placement=1, vNums = 1)
  tree.drawTree(color='red', vNums = 1, placement = 0)
  ```
  
  <p align="center" >
    <img src="https://i.imgur.com/O2EvuVa.png" height="300"
  </p>
    
<b>Example: Overlapping Trees<b>
  ```
  tree=randOrdered(8)
  tree.drawTree(color='#8ea164', vNums = 1)
  tree2 = OrderedTree([[1,8], [1,2], [3,8], [3,7], [3,6], [4,6], [5,6]])
  tree2.drawTree(color='#d49844', placement=0.03, style=':')

  ```
  
  <p align="center" >
    <img src="https://i.imgur.com/MtJt8f0.png" height="300"
  </p>
    
### Drawing Polygons
`drawPolygon(tree, **kwargs)` is the function used to draw a polygon given an OrderedTree object with keyword arguments that give the user the option to alter the design of the polygon. Possible keyword arguments include:
- color= ('color' or 'hexcode')
  - The color for the entire polygon, external and internal lines
  - If no color is specified, a random color will be chosen
- innerColor=
  - The color of the internal lines of the polygon
- outerColor=
  - The color of the external lines of the polygon
- style= ('', ' ', 'None', '--', '-.', '-', ':')
  - The linestyle of the entire polygon, external and internal lines
  - If no style is specified, a solid line will be drawn
- innerStyle= ('', ' ', 'None', '--', '-.', '-', ':')
  - The linestyle of the internal lines of the polygon
- outerStyle= ('', ' ', 'None', '--', '-.', '-', ':')
  - The linestyle of the external lines of the polygon
- thickness=
  - The linewidth of the entire polygon, external and internal lines
- innerThickness=
  - The linewidth of the internal lines of the polygon
- outerThickness=
  - The linewidth of the external lines of the polygon
- placement= 
  - If no placement is specified, polygon is drawn in placement 0
  - `placement = 1` will draw the second polygon to the right side of the first tree
  - To draw overlapping polygons, allocate 0.03 between placements. ex: `placement = 0` and `placement = 0.03` draws overlapping polygons
- dottedLine=[interval1,interval2]
  - Draws a dotted line given an interval.

<b>Example 1<b>

  ```
  tree = OrderedTree(dictToInt({1: [3, 5, 10], 2: [3], 4: [5], 6: [7, 10], 8: [9, 10]})) #brings in tree and turns into a list of lists through a helper function
  tree.drawPolygon(color='#0d4b54', outerThickness='3', innerThickness='1')
  tree1= randOrdered(10) #creates a randomly generated tree of 10 leaves
  tree1.drawPolygon(placement=1, innerStyle=':', innerColor='orange', outerColor='#d94f0b')
  tree2= randOrdered(10)
  tree2.drawPolygon(placement=2)
  ```
  
<p align="center">
  <img src="https://i.imgur.com/ZoVDAw0.png" height="250">
</p>
  
  - This function can also be used to draw overlapping polygons by using different colors when calling the `drawPolygon(tree, **kwargs)` function.
  
  <b>Example 2<b>
  
  ```
  tree = OrderedTree([[1,7], [2,6], [2,7], [3,5], [3,6], [4,5]])
  tree1= randOrdered(7)
  tree.drawPolygon(color='red')
  tree1.drawPolygon(color='blue', innerStyle=':', outerStyle='-',placement=0.03, thickness=1)

  ```
  
 <p align="center">
  <img src="https://i.imgur.com/Zh2FhJ8.png" height="300">
 </p>

    
 ### Drawing Tree Inside Polygons
`drawPolygonTree(tree, **kwargs)` is the function used to draw a tree within a polygon given an OrderedTree object with keyword arguments that give the user the option to alter the design of the polygon. Most of the keywords are similar to that of the Draw Polygon function with additional keywords including: 
- treeColor= ('color' or 'hexcode')
  - The color of the tree inside polygon
  - If no color is specified, default is red
- treeStyle= ('', ' ', 'None', '--', '-.', '-', ':')
  - linestyle of the tree lines inside polygon 
- treeThickness=
  - The linewidth of the tree lines inside polygon
  - If no number is specified, default is 1.5
    
<b>Examples<b>
  ```
  test1 = OrderedTree([[1,2],[1,4],[3,4]])
  test2 = OrderedTree([[1,2],[1,4],[1,5],[3,4]])
  test3 = OrderedTree([[1,3],[1,5],[1,6],[1,8],[2,3],[4,5],[7,8]])
  test4 = OrderedTree([[1,2],[1,3],[1,14],[4,14],[5,11],[5,12],[5,13],[5,14],[6,7],[6,11],[8,9],[8,11],[10,11]])
  
  test1.drawPolygonTree(placement=0)
  test2.drawPolygonTree(placement=1, treeStyle='-.')
  test4.drawPolygonTree(placement=2, treeStyle='--', treeColor='blue')
  test3.drawPolygonTree(placement=3, treeColor='green', treeThickness = 3)
  
  plt.show()
  ```
<p align="center">
  <img src="https://i.imgur.com/EwnnSbR.png" height="300">
</p>
  
    
