import webdev
import os
import json
import math

allPages = {}
totalPages =0
websiteName =""
def checkFileDir():
    if not os.path.exists("pageFiles"):
        os.makedirs("pageFiles")
    if not os.path.exists("pageFreqFiles"):
        os.makedirs("pageFreqFiles")

def get_text(content, link):

    webpageName = content[content.index("itle>") + 5: content.index("</tit")]

    global totalPages
    global websiteName
    totalPages += 1

    linkStart = content.find('</p>')
    linkEnd = content.find('</body>', linkStart)

    outLinks = content[linkStart + 5: linkEnd-1]
    outLinks = outLinks.strip(" ").split()
    links = []

    start = content.find("<p>")
    filePath = os.path.join("pageFiles", webpageName + ".json")
    freqFilePath = os.path.join("pageFreqFiles", webpageName + "TF.json")
    dict = {}
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

    with open(freqFilePath, "w") as fp:
        json.dump(TFDict, fp)
    fp.close()

    dict["Title"] = webpageName
    for x in outLinks:
        if x != '<a':
            link = x[x.index("ref=\".") + 7: x.index("\">")]
            links.append(websiteName + link)
            addIncoming(websiteName + link,webpageName)

    fhand = open(os.path.join("pageFiles", webpageName + ".json"))
    thisdict = json.load(fhand)
    fhand.close()

    dict.update(thisdict)

    dict["URL"] = websiteName + link
    dict["Total Words"] = totalWords
    dict['outgoingLinks'] = links

    with open(filePath, "w") as fp:
        json.dump(dict, fp)
    fp.close()


def addIncoming(addLink,link):
    global websiteName
    fileName = os.path.join("pageFiles", link +'.json')
    if os.path.exists(fileName):
        dict = json.load(open(fileName))
    else:
        dict={}

    if 'incomingLinks' in dict:
        dict['incomingLinks'].append(addLink)
    else:
        dict['incomingLinks'] = [addLink]

    with open(fileName, "w") as fp:
        json.dump(dict, fp)
    fp.close()

def crawler(seed):

    global allPages
    global websiteName
    allPages[seed] = ""
    page = webdev.read_url(seed)
    get_text(webdev.read_url(seed), seed)

    length = 0

    while len(allPages) > length:

        start = page.find("href=\"")

        length = len(allPages)

        while start > 0:
            end = page.find(".html", start)
            link = websiteName + page[start + 8:end + 5]

            if link not in allPages:
                print("crawling " + link)
                crawler(link)
            start = page.find("href=\"", end)

def crawl(seed):
    import time
    global allPages
    global totalPages
    global websiteName
    allPages = {}
    totalPages = 0
    checkFileDir()
    websiteName = seed[0:seed.rfind("/") +1]

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
            if i == "Title":
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
            moretfData[k + "IDF"] = math.log(1 + tfData[k], 2) * idfData[k.strip("TF") + "IDF"]
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

#crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html")
#base url should be the same as page rank - page rank will not work unless urls are exactly the same i.e http vs https
