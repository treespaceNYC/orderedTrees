# #import orderedTree
#
# #Create a new file "test.py" with all the examples/tests that imports orderedTree
#
# #What happens if the input is NOT sorted? What do we do with it?
# #input1 = [1,2],[1,3],[1,4][1,6][1,5]
# #dictionaryform = d{1:[2,3,4,6,5]}
#
# #Sort values when put in dictionary *must have lists for it to work* *Not tuples*
# #sorted.values()
#
#
# #Question 1: Can the input test cases be regrouped to be ordered?
#
#
#     #Test cases that are NOT ordered but can be ordered
# notorderedN1 = "(((((2,1),3),4),5),6)"
# notorderedI1 = "[1,2],[1,3],[1,4][1,5][1,6]"
#
#
#     #Test cases that are NOT ordered and CANNOT be ordered
# notorderedN1 = "(((((1,3),2),4),5),6)"
# notorderedI1 = "[1,3],[1,2],[1,4][1,5][1,6]"
#
#
# #Question 2: What if input is a string in newick form?
#
#
#     #Newick Form Test cases
# newick1 = "(((((1,2),3),4),5),6)"
#
# newick2 = "((((1,(2,3)),4),5),6)"
#
# newick3 = "((1,(2,3)),((4,5),6))"
#
# newick4 = "((1,2),(((3,4),5),6))"
#
#
# #Question 3: What if the input is a string of lists in interval form or a list of lists?
#
#     #Interval Form Test cases
# interval_list1  = [ [1,2],[1,3],[1,4][1,5][1,6] ]
# interval_string1  = "[1,2],[1,3],[1,4],[1,5],[1,6]"
#
# interval_list2  = [ [1,2],[1,4],[1,6],[3,4],[5,6] ]
# interval_string2  = "[1,2],[1,4],[1,6],[3,4],[5,6]"
#
# interval_list3 = [ [1,2],[1,6],[3,4],[5,6] ]
# interval_string3  = "[1,2],[1,6],[3,4],[5,6]"
#
#
#
import re
from collections import OrderedDict, defaultdict



def newick2interval(newick):
    intervals = []
    commaCount = newick.count(",")
    while commaCount!=1:
        m = re.search(",?\(\d+,\d+\),?",newick)
        groupPos = m.span() # tuple in the form (pos, pos)

        # Right sibling pair
        if m.group()[0] == ",":
            # Find position of "," to split string
            commaPos = groupPos[0]+m.group().rindex(",")

            # Left number
            left = int(newick[groupPos[0]+2:commaPos])
            # Right number
            right = int(newick[commaPos+1:groupPos[1]-1])

            # Add to interval then shrink string
            intervals.append([left,right])
            newick = newick[:groupPos[0]+1] + newick[commaPos+1:groupPos[1]-1] + newick[groupPos[1]:]

        # Left sibling pair
        else:
            # Find position of "," to split string
            commaPos = groupPos[0]+m.group().index(",")

            # Left number
            left = int(newick[groupPos[0]+1:commaPos])
            # Right number
            right = int(newick[commaPos+1:groupPos[1]-2])

            # Add to interval then shrink string
            intervals.append([left,right])
            newick = newick[:groupPos[0]] + newick[groupPos[0]+1:commaPos] + newick[groupPos[1]-1:]
        commaCount-=1
    # String is now in the form (\d,\d)

    # Find position of "," to split string
    commaPos = newick.index(",")

    # Left number
    left = int(newick[1:commaPos])
    # Right number
    right = int(newick[commaPos+1:len(newick)-1])

    # Add to interval then turn into dictionary
    intervals.append([left,right])
    return intervals
    # d = defaultdict(list)
    # for k, v in intervals:
    #     d[k].append(v)
    # return OrderedDict(sorted(d.items()))#sort and return


from collections import OrderedDict, defaultdict
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

# s = "(((1,2),3),(4,(5,6)))"
# s = "(((((1,2),3),4),5),6)"
# s = "(((((1,(2,3)),4),5),6),(7,(8,9)))"
# s ="((((1,(2,3)),4),5),6)"
# s ="(((1,2),(3,4)),(5,6))"
# s ="(1,(2,(3,(4,(5,(6,7))))))"
s ="(1,(2,(3,(4,(5,(6,(7,(8,(9,10)))))))))"

print(intervalNewick(newick2interval(s)))
