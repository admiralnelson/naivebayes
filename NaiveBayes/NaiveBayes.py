import os
import pickle
import csv
from collections import Counter

PATH = "NaiveBayes/TrainsetTugas1ML.csv"
#TESTPATH = "NaiveBayes/TestTugas1ML.csv"
TESTPATH = "NaiveBayes/TrainsetTugas1ML.csv"
TABLEPATH = "NaiveBayes/Table.dat"
DEBUG = True

data = []
testData = []
cols = []

def is_sublist(a, b):
    if not a: return True
    if not b: return False
    return b[:len(a)] == a or is_sublist(a, b[1:])

def GenerateTable(d):
    #for key, val in d.items():
    #    for k,v in val.items():
    #        print(k, " ", v)
    with open(TABLEPATH, "wb") as f:
        pickle.dump(d,f)
        f.close()
    return None

def ProcessData():
    with open(PATH) as csvfile:
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
            #print(key, val)

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
        dic["totalData"] = len(data)
        return dic         

def Learn():
    print(os.getcwd())
    t = ProcessData()
    GenerateTable(t)
    if(DEBUG):
        for d in data:
            d.pop(0)
            print(d)
    
def Classify(data):
    totalData = 0
    with open(TABLEPATH, 'rb') as file:
        classifierData = pickle.load(file)

    totalData = classifierData["totalData"]
    del classifierData["totalData"]
    with open(TESTPATH) as csvfile: 
        reader = csv.reader(csvfile, quotechar="|")
        collums = next(reader)
        collums.pop()
        for c in collums:
            cols.append((c, []))
        for row in reader:
            testData.append(row)
            testData[testData.index(row)].pop(0)
            testData[testData.index(row)].pop()
        #print(classifierData)
        #print(testData)

        for row in testData:
            classifierAttr = list(classifierData)
  
            totalValue = 0

            classKey = classifierData[classifierAttr[-1]]
            evaluatedClass = dict()
            klassIndex = 0
            for k in classKey.keys():
                evaluatedClass[k] = 0
                i = 0
                totalValue = 1
                for attr in row:
                    key = classifierAttr[i]
                    attrToMatch = classifierData[key]
    

                    klass = attrToMatch[attr]       


                    klass[klassIndex]
                    totalValue *= klass[klassIndex][0]/klass[klassIndex][1]
                    #totalValue *= classifyTarget[0]/classifyTarget[1]
                    i+=1
                evaluatedClass[k] = totalValue
                klassIndex += 1
            result = max(evaluatedClass, key=evaluatedClass.get)
            row.append(result)
    if(DEBUG):
        for d in testData:
            print(d)

#Learn()
Classify(None)