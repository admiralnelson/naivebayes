import os
import re
import sys
import pickle
import csv
from collections import Counter

PATH = "TrainsetTugas1ML.csv"
TESTPATH = "TestTugas1ML.csv"
#TESTPATH = "NaiveBayes/TrainsetTugas1ML.csv"
TABLEPATH = "Table.dat"
DEBUG = False
LEARN = False

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
    print("Hasil pembelajaran ditulis ke" + os.getcwd() + "/" + TABLEPATH)

def ProcessData():
    with open(PATH) as csvfile:
        print("Membaca file " + os.getcwd() + "/" + PATH)
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

        try:
            del dic["id"]
        except Exception as identifier:
            print("WARN: field ID tidak ada")
        
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
        print("Learning OK")
        return dic         

def WriteCsv(path, data, label = []):
    wtr = csv.writer(open (path, 'w'), delimiter=',', lineterminator='\n')
    data.insert(0, label)
    for x in data : 
        wtr.writerow (x)
    print("File ditulis di lokasi " + os.getcwd() + "/" + path)

def Learn():
    t = ProcessData()
    GenerateTable(t)
    if(DEBUG):
        for d in data:
            d.pop(0)
            print(d)
    
def Classify():
    totalData = 0
    with open(TABLEPATH, 'rb') as file:
        classifierData = pickle.load(file)

    totalData = classifierData["totalData"]
    idArray = []
    del classifierData["totalData"]
    with open(TESTPATH) as csvfile: 
        reader = csv.reader(csvfile, quotechar="|")
        collums = next(reader)
        collums.pop()
        for c in collums:
            cols.append((c, []))
        for row in reader:
            testData.append(row)
            idArray.append(testData[testData.index(row)].pop(0))
            testData[testData.index(row)].pop()

        no = 0
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
            
            row.insert(0, idArray[no])
            row.append(result)
            
            no += 1
    if(DEBUG):
        for d in testData:
            print(d)
    
    print("Klasifikasi OK")
    return testData

def CheckArgv():
    global LEARN
    global DEBUG
    if(len(sys.argv) == 1):
        print("Set argument learning=true to learn, debug=true for debug")
    if("learning=true" in sys.argv): LEARN = True
    if("debug=true" in sys.argv): DEBUG = True
    

CheckArgv()
if(LEARN): Learn()
d = Classify()
WriteCsv("TebakanTugas1ML.csv", d, label=["id","age","workclass","education","marital-status","occupation","relationship","hours-per-week","income"])