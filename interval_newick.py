from collections import OrderedDict, defaultdict
# things = [ [1,2], [1,3]  ]
# things = [[1, 3], [1, 4], [1, 5], [1, 6], [1, 9], [2, 3], [7, 9], [8, 9] ]
# things = [[1, 2], [1, 3], [1, 4]]
things = [[1, 6], [2, 3], [2, 6], [4, 5], [4, 6]]
d = { 1:[2,3] }
def interval2newick(interval):
    intervals = defaultdict(list)
    for k, v in interval:
        intervals[k].append(v)
    #turn input into a dictionary
    minMax = {}
    # Using number of values of each key
    # to find how nested it is
    for key, val in intervals.items():
        intervals[key] = sorted(intervals[key])
        for i in val:
            minMax.setdefault(key,["(",0])
            #set key to all the min leaves, and then the values to the open paren since we use those b4 mins and then the counter for how many
            minMax.setdefault(i,[")",0])
            #set the key to all the max leaves and then set the values to closing paren and set the counter for the number of closing paren to print

            minMax[i][1]+=1
            #if we see max, we add one to its counter
            minMax[key][1]+=1
            #if we see a value for the min, add one to the counter
    minMax = OrderedDict(sorted(minMax.items()))
    result = ""
    for key, val in minMax.items():
    #formatting what we stored into a string to return
        if val[0] == "(":
            result+= (val[0]*val[1]) + str(key) + ","
        else:
            result+= str(key) + (val[0]*val[1]) + ","
    return result[:-1]
print(interval2newick(things))
