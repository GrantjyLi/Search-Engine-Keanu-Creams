import os

urlToIndex={}
indexToURL={}
matrix=[]

def createMap(url):
    global urlToIndex
    global indexToURL
    
    files = os.listdir('pageFiles')

    count = 0
    for x in files:
        urlToIndex[url+x[0:3]+'.html'] = count
        indexToURL[count] = url+x[0:3]+'.html'
        count+=1



def createMatrix():
    global urlToIndex
    global indexToURL
    for x in range (len(urlToIndex)):
        matrix.append([0]*len(urlToIndex))


createMap('chicken/')
print(createMatrix())