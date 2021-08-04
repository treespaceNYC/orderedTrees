# OrderedTrees

Code for storing and comparing ordered trees.

Stores a tree in dictionary format using defaultdict from collections.
- Dictionary has left intervals as the keys and right intervals in a list for each key.

Overrides print function to print the stored tree and number of leaves.

Overrides equals operator in order to allow for comparison of two trees.


## Dependencies
- Python 3.9.x
- Shapely
  - `pip install Shapely`
- Matplotlib
  - `pip install -U matplotlib`

## Installation
Download orderedTree.py and place it in your working directory

## Examples

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
`randInterval(1,5)` will create random intervals based on these two ints. `randOrdered([1,5])` will do the same.
  - `randInterval(1,4)` may result in [[1,2],[3,4]] or [[1,3]] or [[3,4]]

- `randOrdered(n)` will create a random OrderedTree object with n leaves.
  - `randOrdered(20)` may create a tree with intervals: \
[1,2], [1,3], [1,14], [1,20], [4,5], [4,8], [4,9], [4,14], [6,8], [7,8], [10,14], [10,11], [12,14], [13,14], [15,16], [15,20], [17.18], [19,20] 
<img src="https://i.imgur.com/lF7d3Hy.png">

### Rotating Trees

### Drawing Trees

### Drawing Polygons
