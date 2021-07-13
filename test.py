#import orderedTree

#Create a new file "test.py" with all the examples/tests that imports orderedTree

#What happens if the input is NOT sorted? What do we do with it?
#input1 = [1,2],[1,3],[1,4][1,6][1,5]
#dictionaryform = d{1:[2,3,4,6,5]}

#Sort values when put in dictionary *must have lists for it to work* *Not tuples*
#sorted.values()


#Question 1: Can the input test cases be regrouped to be ordered?


    #Test cases that are NOT ordered but can be ordered 
notorderedN1 = "(((((2,1),3),4),5),6)"
notorderedI1 = "[1,2],[1,3],[1,4][1,5][1,6]"


    #Test cases that are NOT ordered and CANNOT be ordered 
notorderedN1 = "(((((1,3),2),4),5),6)"
notorderedI1 = "[1,3],[1,2],[1,4][1,5][1,6]"


#Question 2: What if input is a string in newick form?
    
    
    #Newick Form Test cases
newick1 = "(((((1,2),3),4),5),6)"

newick2 = "(((1,(2,3),4),5),6)"

newick3 = "(((1,(2,3),(4,5),6)))"

newick4 = "(((1,2),(3,4),5),6)"


#Question 3: What if input is a string of lists in interval form or a list of lists?

    #Interval Form Test cases
interval_list1  = [ [1,2],[1,3],[1,4][1,5][1,6] ]
interval_string1  = "[1,2],[1,3],[1,4],[1,5],[1,6]"

interval_list2  = [ [1,2],[1,4],[1,6],[3,4],[5,6] ]
interval_string2  = "[1,2],[1,4],[1,6],[3,4],[5,6]"

interval_list3 = [ [1,2],[1,6],[3,4],[5,6] ]
interval_string3  = "[1,2],[1,6],[3,4],[5,6]"
