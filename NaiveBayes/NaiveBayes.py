
import csv
from collections import Counter


data = []
cols = []

def is_sublist(a, b):
    if not a: return True
    if not b: return False
    return b[:len(a)] == a or is_sublist(a, b[1:])

def GenerateTable(d):
    for key, val in d.items():
        for k,v in val.items():
            print(k, " ", v)

    print("")
    return None

def ProcessData():
    with open("TrainsetTugas1ML.csv") as csvfile:
        reader = csv.reader(csvfile, quotechar="|")
        collums = next(reader)
        for c in collums:
            cols.append((c, []))
    
        for row in reader:
            data.append(row)
            for i  in range(0, len(row)):
                cols[i][1].append(row[i])


        #print(cols)

        dic  = dict()
        for k in cols:
            dic[k[0]] = dict(Counter(k[1]))

        del dic["id"]
        #print(dic)

        ##################TOTAL
        foundZero = False
        for key,val in dic.items():
            print(key, val)

            for k, v in val.items():
            
            
                classifier = list(dic.keys())[-1]
                classifierLabel = list(dic[classifier].keys())
                classifierColIndex = 1 + list(dic.keys()).index(classifier)
            
                colIndex = 1 + list(dic.keys()).index(key)
            
                count = []
                val[k] = []
                for c in classifierLabel:
                    if(colIndex < classifierColIndex):
                        count.append([len([elem for elem in data if elem[colIndex] == k  and elem[classifierColIndex] == c]), dic[classifier][c]])
                if colIndex >= classifierColIndex:
                    count.append([len([elem for elem in data if elem[colIndex] == k]), len(data)])
            
                val[k] = count
                for tpl in count:
                    #print(tpl)
                    if(tpl[0] == 0):
                        foundZero = True
                # print("sub item ", k, val[k])
            
                #if(v[0] == 0): foundZero = True
        ##################TOTAL

        ##################LAPLACIAN CORRECTION




        ##################LAPLACIAN CORRECTION
 

        if(foundZero):
            for key,val in dic.items():  
                for k, v in val.items():
                    for j in range(0, len(val[k])):
                            for i in range(0, len(val[k][j])):  
                                    val[k][j][i] += 1
                print("=",key, val)
                    #if(v[0] == 0): foundZero = True
        return dic;           

def Main():
    t = ProcessData()
    GenerateTable(t)
    

Main()