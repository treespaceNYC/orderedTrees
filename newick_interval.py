from collections import defaultdict
### Probably not balanced
snewick = "(((((1,(2,3)),4),5),6),(((7,(8,9)),(((10,11),12),((13,14),15))))"
# snewick = "(1,(2,(3,(4,(5,(6,(7,(8,(9,10)))))))))" ### works fine
 
### gets digits > 1
def getNum(snewick,i,one,truth):
    count = i
    num = ""
    while snewick[count].isnumeric():
        num+=snewick[count]
        count+=one
    if truth:
        num = num[::-1]
    num = eval(num)
    return num, count
 
### loops through both sides of the root and calculates parenthesis to find how many intervals for each num
def newickToInterval(snewick):
    total = 0
    d = defaultdict(int)
    par = 0
    pos = 0
    mins = []
    maximums = []
    max = 0
    intervals = []
    ### works fine
    # for i in range(len(snewick)-1):
    i = 0
    while i < len(snewick):
        ### first half is done
        if total == 1 and snewick[i] == ",":
            pos = i
            break
        if snewick[i] == "(":
            total+=1
            par+=1
            if snewick[i+1].isnumeric():
            ### parse large digit
                num = getNum(snewick,i+1,1,False)[0]
                maximums.append(num)
            ### get num of parenthesis for digit
                d[num]=par
                par=0
        elif snewick[i] == ")":
            total-=1
            for key, val in d.items():
            ### one less interval for each num
                d[key]-=1
            ### no more intervals left
                if val == 0:
                    maximums.remove(key)
            if snewick[i-1].isnumeric():
                num = getNum(snewick,i-1,-1,True)[0]
                for j in maximums:
                    intervals.append([j,num])
        i+=1
    
    ### doesnt work properly, in the above example it will get [8,15] rather than [7,15]
    i = len(snewick)-1
    while i >= pos:
        # print(i)
        if snewick[i] == "(":
            total-=1
            if snewick[i+1].isnumeric():
                num = getNum(snewick,i+1,1,False)[0]
                for j in mins:
                    intervals.append([num,j])
            ### will always be a [min,max] interval
                if num > max:
                    max = num
                    intervals.append([1,max])
                for key, val in d.items():
                    d[key]-=1
                    if d[key] == 0:
                        mins.remove(key)
                        # print()
        elif snewick[i] == ")":
            total+=1
            par+=1
            if snewick[i-1].isnumeric():
                num, i = getNum(snewick,i-1,-1,True)
                d[num]=par
                par=0
                if num > max:
                    max = num
                    intervals.append([1,max])
                    d[max]-=1
                    if d[max] == 0:
                        mins.remove(max)
                mins.append(num) 
        # print(d)
        i-=1
    return intervals
