import os

urlToIndex={}
indexToURL={}

def createMap(url):
    global urlToIndex
    global indexToURL
    
    files = os.listdir('pageFiles')

    count = 0
    for x in files:
        urlToIndex[url+x[0:3]+'.html'] = count
        indexToURL[count] = url+x[0:3]+'.html'
        count+=1



