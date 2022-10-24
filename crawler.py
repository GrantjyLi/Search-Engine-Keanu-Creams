import webdev
import os
import json
import math

allPages = []
totalPages =0
def checkFileDir():
    if not os.path.exists("pageFiles"):
        os.makedirs("pageFiles")
    if not os.path.exists("pageFreqFiles"):
        os.makedirs("pageFreqFiles")

def get_text(content, websiteName):
    global totalPages
    totalPages += 1

    linkStart = content.find('</p>')
    linkEnd = content.find('</body>', linkStart)

    outLinks = content[linkStart + 5: linkEnd-1]
    outLinks = outLinks.strip(" ").split()
    links = []

    for x in outLinks:
        if x != '<a':
            links.append("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/" + x[8:16])#This will not work for other urls
            addIncoming("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/" + x[8:16],"http://people.scs.carleton.ca/~davidmckenney/tinyfruits/" + websiteName)


    start = content.find("<p>")
    filePath = os.path.join("pageFiles", websiteName+".json")
    freqFilePath = os.path.join("pageFreqFiles", websiteName + "TF.json")
    if os.path.exists("pageFiles/"+websiteName+'.json'):
        dict = json.load(open(filePath))
    else:
        dict={}
    totalWords =0

    while start > 0:
        end = content.find("</p>", start)
        words = content[start + 3: end]

        words = words.strip("\n").split()
        for i in words:
            if i not in dict:
                dict[i] = 0
            dict[i] += 1
        totalWords += len(words)
        start = content.find("<p>", end)
    TFDict ={}

    for i in dict:
        if type(dict[i]) is int: 
            TFDict[i + "TF"] = dict[i]/totalWords

    dict["Total Words"] = totalWords
    dict['outgoingLinks'] = links

    with open(filePath, "w") as fp:
        json.dump(dict, fp)
    fp.close()

    with open(freqFilePath, "w") as fp:
        json.dump(TFDict, fp)
    fp.close()


def addIncoming(addLink,link):

    websiteName = addLink[0:len(link) - len("N-X.html")-1]
    webpageName = addLink.strip(websiteName)
    fileName = os.path.join("pageFiles", webpageName[5:8] +'.json')

    if os.path.exists("pageFiles/"+webpageName[5:8]+'.json'):
        dict = json.load(open("pageFiles/"+webpageName[5:8]+'.json'))
    else:
        dict={}

    if 'incomingLinks' in dict:
        dict['incomingLinks'].append(link)
    else:
        dict['incomingLinks'] = [link]

    with open(fileName, "w") as fp:
        json.dump(dict, fp)
    fp.close()

def crawler(seed):
    checkFileDir()
    global allPages
    allPages.append(seed)
    page = webdev.read_url(allPages[-1])
    websiteName = seed[0:len(seed) - len("N-X.html")]
    webpageName = seed.strip(websiteName)
    get_text(webdev.read_url(seed), webpageName)

    length = 0

    while len(allPages) > length:

        start = page.find("href=\"")

        length = len(allPages)

        while start > 0:
            end = page.find(".html", start)
            link = websiteName + page[start + 8:end + 5]

            if not link in allPages:
                print("crawling " + link)

                crawler(link)
            start = page.find("href=\"", end)

def crawl(seed):
    import time
    global allPages
    global totalPages
    allPages = []
    totalPages = 0

    start = time.time()
    checkFileDir()
    for i in os.listdir("pageFiles"):
        os.remove(os.path.join("pageFiles", i))
    for i in os.listdir("pageFreqFiles"):
        os.remove(os.path.join("pageFreqFiles", i))

    crawler(seed)

    itemPages ={}
    for i in os.listdir("pageFiles"):
        fHand = open(os.path.join("pageFiles", i))
        data = json.load(fHand)
        fHand.close()
        for i in data:
            if i == "Total Words":
                break
            if i not in itemPages:
                itemPages[i] =0
            itemPages[i] +=1

    idfData ={}
    for i in itemPages:
        idfData[i + "IDF"] = math.log(totalPages/(1+itemPages[i]), 2)


    for i in os.listdir("pageFreqFiles"):
        fHand = open(os.path.join("pageFreqFiles", i))
        tfData = json.load(fHand)
        fHand.close()
        moretfData ={}
        for k in tfData:
            moretfData[k + "IDF"] = math.log(1 + tfData[k]) * idfData[k.strip("TF") + "IDF"]
        tfData.update(moretfData)
        with open(os.path.join("pageFreqFiles", i), "w") as fp:
            json.dump(tfData, fp)
        fp.close()

    with open(os.path.join("pageFreqFiles", "IDFData.json"), "w") as fp:
        json.dump(idfData, fp)
    fp.close()

    with open(os.path.join("pageFreqFiles", "wordPageCount.json"), "w") as fp:
        json.dump(itemPages, fp)
    fp.close()

    end = time.time()
    print(end - start)
    return totalPages

crawler("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html")