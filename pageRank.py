from operator import index
import os
import json
import math

#Global Variables
urlToIndex={}
indexToURL={}
matrix=[]
alpha = .1
length = 0

#Functions
def resetData():
    global urlToIndex
    global indexToURL
    global matrix
    global length
    if os.path.isdir('pageRank'):
        for i in os.listdir("pageRank"):
            os.remove(os.path.join("pageRank", i))
    urlToIndex={}
    indexToURL={}
    matrix = []
    length=0



def mult_scalar(matrix, scale):
	resMatrix = matrix
	for i in range(len(matrix)):
		for j in range(len(matrix[i])):
			resMatrix[i][j] *= scale
	return resMatrix


def mult_matrix(a, b):
	if ((len(b) != len(a[0])) or (len(a) == 0) or (len(b) ==0) or (len(a[0])==0) or (len(b[0]) ==0)):
		return None

	resMatrix = []
	for i in range (len(a)):
		resMatrix.append([])

	for i in range(len(b[0])):#For each column in matrix b
		for j in range (len(a)):#For each row in matrix a
			currSum=0
			for k in range (len(a[0])):#For each element in row j
				currSum+=a[j][k]*b[k][i]#Multiply the element in j row of 'a' by the corresponding value in i column of 'b' and add it to currSum
			resMatrix[j].append(currSum)#add currSum to the result Matrix
	return resMatrix


def euclidean_dist(a, b):
    if len(a[0]) != len(b[0]):
        return None
	
    sum=0
    for i in range (len(a[0])):
        sum+=(a[0][i]-b[0][i])**2
        return (sum)**(1/2)


def fetchURL(file):
    dict = json.load(open(os.path.join("pageFiles", file)))
    return dict['URL']


def createMap():
    global urlToIndex
    global indexToURL
    global length
    
    files = os.listdir('pageFiles')

    count = 0
    for x in files:
        urlToIndex[fetchURL(x)] = count
        indexToURL[count] = fetchURL(x)
        count+=1
    length = len(indexToURL)
    
    
def createMatrix():
    global urlToIndex
    global indexToURL
    for x in range (len(urlToIndex)):
        matrix.append([0]*len(urlToIndex))

    files = os.listdir('pageFiles')
    
    for x in files:
        dict = json.load(open(os.path.join("pageFiles", x)))
        for y in dict['outgoingLinks']:
            matrix[urlToIndex[fetchURL(x)]][urlToIndex[y]] = 1
            matrix[urlToIndex[y]][urlToIndex[fetchURL(x)]] = 1


def randomProbability():
    for x in matrix:
        numX = 0
        numIndex = []
        for y in range (len(x)):
            if x[y] == 1:
                numX+=1
                numIndex.append(y)
        if numX == 0:
            for y in range (len(x)):
                x[y] = 1/length
        else:
            for z in numIndex:
                x[z] = 1/numX

def modAlpha():
    global matrix
    global length
    matrix = mult_scalar(matrix, 1 - alpha)

    for x in matrix:
        for y in range(len(x)):
            x[y] += alpha/length


def addCurrVector(currVector):
    for x in range(length-1):
        currVector.append(0)
    return [currVector]


def piMultiplication():
    global matrix
    global length

    prevVector = [[100]*length]
    currVector = [1]
    currVector = addCurrVector(currVector)
    distance = (euclidean_dist(prevVector,currVector))
    count=0

    while distance > .001:
        prevVector = currVector
        currVector = mult_matrix(currVector, matrix)
        count+=1
        distance = (euclidean_dist(prevVector,currVector))
    
    return currVector


def saveData(values):
    if not os.path.exists("pageRank"):
        os.makedirs("pageRank")
    filePath = os.path.join("pageRank","data.json")
    dict={}
    for x in range (len(values[0])):
        dict[indexToURL[x]] = values[0][x]

    with open((filePath), "w") as fp:
        json.dump(dict, fp)
    fp.close()

def altSaveData(values):
    if not os.path.exists("pageRank"):
        os.makedirs("pageRank")
    
    for i in range (len(values[0])):
        fileName = indexToURL[i]
        filePath=open(os.path.join("pageRank", fileName[-8:-5]+'.txt'), 'a')
        filePath.write(str(values[0][i]))
        filePath.close()



#Main Function       
def pageRank():
    resetData()
    createMap()
    createMatrix()
    randomProbability()
    modAlpha()
    piData= piMultiplication()
    saveData(piData)
    altSaveData(piData)
