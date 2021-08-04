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

It's also possible to create both random intervals and random OrderedTree objects. \
`randOrdered(list)`

### Drawing Trees

### Drawing Polygons

### Rotating Trees
