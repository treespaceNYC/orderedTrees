def intervalNewick(interval):
    intervals = defaultdict(list)
    for k, v in interval:
        intervals[k].append(v)
    minMax = {}
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
