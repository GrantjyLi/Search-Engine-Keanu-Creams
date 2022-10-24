import os
import json

urlToIndex = {}
indexToURL = {}
matrix = []
alpha = .1
length = 0


def mult_scalar(matrix, scale):
    resMatrix = matrix
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            resMatrix[i][j] *= scale
    return resMatrix


def mult_matrix(a, b):
    if ((len(b) != len(a[0])) or (len(a) == 0) or (len(b) == 0) or (len(a[0]) == 0) or (len(b[0]) == 0)):
        return None

    resMatrix = []
    for i in range(len(a)):
        resMatrix.append([])

    for i in range(len(b[0])):  # For each column in matrix b
        for j in range(len(a)):  # For each row in matrix a
            currSum = 0
            for k in range(len(a[0])):  # For each element in row j
                currSum += a[j][k] * b[k][
                    i]  # Multiply the element in j row of 'a' by the corresponding value in i column of 'b' and add it to currSum
            resMatrix[j].append(currSum)  # add currSum to the result Matrix
    return resMatrix

def euclidean_dist(a,b):
	if len(a[0]) != len(b[0]):
		return None
	
	sum=0
	for i in range (len(a[0])):
		sum+=(a[0][i]-b[0][i])**2
	return (sum)**(1/2)

def createMap(url):
    global urlToIndex
    global indexToURL
    global length

    files = os.listdir('pageFiles')

    count = 0
    for x in files:
        urlToIndex[url + x[0:3] + '.html'] = count
        indexToURL[count] = url + x[0:3] + '.html'
        count += 1
    length = len(indexToURL)


def createMatrix():
    global urlToIndex
    global indexToURL
    for x in range(len(urlToIndex)):
        matrix.append([0] * len(urlToIndex))


def populateMatrix(url):
    global matrix
    files = os.listdir('pageFiles')

    for x in files:
        dict = json.load(open(os.path.join("pageFiles", x)))
        for y in dict['outgoingLinks']:
            matrix[urlToIndex[url + x[0:3] + '.html']][urlToIndex[y]] = 1
            matrix[urlToIndex[y]][urlToIndex[url + x[0:3] + '.html']] = 1


def randomProbability():
    for x in matrix:
        numX = 0
        numIndex = []
        for y in range(len(x)):
            if x[y] == 1:
                numX += 1
                numIndex.append(y)
        if numX == 0:
            for y in range(len(x)):
                x[y] = 1 / length
        else:
            for z in numIndex:
                x[z] = 1 / numX


def modAlpha():
    global matrix
    global length
    matrix = mult_scalar(matrix, 1 - alpha)

    for x in matrix:
        for y in range(len(x)):
            x[y] += alpha / length


def addCurrVector(currVector):
    for x in range(length - 1):
        currVector.append(0)
    return [currVector]


def piMultiplication():
    global matrix
    global length

    prevVector = [[100, 100, 100, 100, 100, 100, 100, 100, 100, 100]]
    currVector = [1]
    currVector = addCurrVector(currVector)
    distance = (euclidean_dist(prevVector, currVector))
    count = 0





createMap('http://people.scs.carleton.ca/~davidmckenney/tinyfruits/')
print(createMatrix())

populateMatrix('http://people.scs.carleton.ca/~davidmckenney/tinyfruits/')

randomProbability()
modAlpha()

print(matrix)