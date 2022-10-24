import os

urlToIndex={}
indexToURL={}
matrix=[]
alpha = .1
length = 0



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
        urlToIndex[url+x[0:3]+'.html'] = count
        indexToURL[count] = url+x[0:3]+'.html'
        count+=1
    length = len(indexToURL)
    
    



def createMatrix():
    global urlToIndex
    global indexToURL
    for x in range (len(urlToIndex)):
        matrix.append([0]*len(urlToIndex))


createMap('chicken/')
print(createMatrix())