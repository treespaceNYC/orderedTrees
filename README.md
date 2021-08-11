# OrderedTrees

Code for storing and comparing ordered trees.

Stores a tree in dictionary format using defaultdict from collections.
- Dictionary has left intervals as the keys and right intervals in a list for each key.

Overrides print function to print the stored tree and number of leaves.

Overrides equals operator in order to allow for comparison of two trees.

## Contributors

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
- No input for an empty constructor 
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
  newTree = rotateRight(tree, [3,6])[0]
  ```
  <p align="center">
    <img src="https://i.imgur.com/Pw6U5SL.png" height="400" width="500">
  </p>

### Drawing Trees
`drawTree(tree, **kwargs)` is the function used to draw trees when given a list of intervals and keyword arguments which allow the user to change the design and placement of the tree. Possible keyword arguments include:
- color= (if no color is specified, it will choose at random)
- style= 
- placement= 
  - `placement = 1.1` will print the second tree to the right side of the first tree
- vNums=(0 or 1)
  - `vNums = 1` means that the tree will be marked with numbers at the bottom of each leaf. Otherwise, it will be an unnumbered tree. 
- scaled=(0 or 1)
  - If there are 2 trees that have different number of leaves, use `scale = 1` to make sure both trees are the same width and height

<b>Example<b>
  ```
  tree = OrderedTree([[1,2], [1,5], [1,8], [3,4], [3,5], [6,7], [6,8]])
  test1 = OrderedTree([[1,8], [1,2], [3,8], [3,7], [3,6], [4,6], [5,6]])
  test1.drawTree(color='blue', placement=1.1, vNums = 1)
  tree.drawTree(color='red', vNums = 1, placement = 0)
  ```
  
  <p align="center" >
    <img src="https://user-images.githubusercontent.com/72881310/128757620-8d32607f-52c2-4389-a538-28fd01c4a7cc.png" height="400" width="1000"
  </p>
    

### Drawing Polygons
`drawPolygon(tree, **kwargs)` is the function used to draw a polygon given a tree in interval form (list of lists) and keyword arguments that allow the user to change the color of the polygon as well as the line style.

<b>Example 1<b>

  ```
  test1 = OrderedTree(dictToInt({1: [3, 5, 10], 2: [3], 4: [5], 6: [7, 10], 8: [9, 10]})) #brings in tree and turns into a list of lists through a helper function
  test1.drawPolygon(color='blue', linestyle='-')
  ```
  
<p align="center">
  <img src="https://user-images.githubusercontent.com/72881310/128402066-2b4ab1d3-3bd1-4550-9294-492d5c60faf8.png" width="500" height="500">
</p>
  
  - This function can also be used to draw overlapping polygons by using different colors when calling the `drawPolygon(tree, **kwargs)` function.
  
  <b>Example 2<b>
  
  ```
  tree = OrderedTree([[1,7], [2,6], [2,7], [3,5], [3,6], [4,5]])
  test1 = OrderedTree(dictToInt({1: [3, 5, 10], 2: [3], 4: [5], 6: [7, 10], 8: [9, 10]}))
  test1.drawPolygon(color='blue', linestyle='-')
  tree.drawPolygon(color='red', linestyle='.')
  ```
  
 <p align="center">
  <img src="https://user-images.githubusercontent.com/72881310/128748398-5bc2b879-6497-4933-893e-d7e480bdaca1.png" width="500" height="500">
 </p>

 
 Some possible keyword arguments that can be controlled by the user are as follows:
 - placement=
 - color= 
 - style=
 - thickness= 
 - innerColor= 
 - outerColor= 
 - innerStyle= 
 - outerStyle= 
 - innerThickness=
 - outerThickness=
 - dottedLine=[interval,interval]
  
