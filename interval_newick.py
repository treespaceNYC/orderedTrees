things = [ [1,2], [1,3]  ]
things = [[1, 3], [1, 4], [1, 5], [1, 6], [1, 9], [2, 3], [7, 9], [8, 9] ]
# things = [[1, 2], [1, 3], [1, 4]]
# things = [[1, 6], [2, 3], [2, 6], [4, 5], [4, 6]]
d = { 1:[2,3] }
def intervalNewick(interval):
    intervals = defaultdict(list)
    for k, v in interval:
        intervals[k].append(v)
    minMax = {}
    # Using number of values of each key
    # to find how nested it is
    for key, val in intervals.items():
        intervals[key] = sorted(intervals[key])
        for i in val:
            minMax.setdefault(key,["(",0])
            minMax.setdefault(i,[")",0])
            minMax[i][1]+=1
            minMax[key][1]+=1
    minMax = OrderedDict(sorted(minMax.items()))
    result = ""
    for key, val in minMax.items():
        if val[0] == "(":
            result+= (val[0]*val[1]) + str(key) + ","
        else:
            result+= str(key) + (val[0]*val[1]) + ","
    return result[:-1]
print(intervalNewick(things))
