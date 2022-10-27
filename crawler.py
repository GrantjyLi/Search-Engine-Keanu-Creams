import webdev
import os
import json
import math
import pageRank
allPages = {}
totalPages =0
def checkFileDir():
    if not os.path.exists("pageFiles"):
        os.makedirs("pageFiles")
    if not os.path.exists("pageFreqFiles"):
        os.makedirs("pageFreqFiles")
    if not os.path.exists("incomingLinks"):
        os.makedirs("incomingLinks")
    if not os.path.exists("pageRank"):
        os.makedirs("pageRank")

def clear_Data():
    global allPages
    global totalPages
    allPages = {}
    totalPages = 0

    checkFileDir()
    for i in os.listdir("pageFiles"):
        os.remove(os.path.join("pageFiles", i))
    for i in os.listdir("pageFreqFiles"):
        os.remove(os.path.join("pageFreqFiles", i))
    for i in os.listdir("incomingLinks"):
        os.remove(os.path.join("incomingLinks", i))
    for i in os.listdir("pageRank"):
        os.remove(os.path.join("pageRank", i))
    

def get_wordCount(content):
    pageDict = {}  # dictionary that hold's a page's important values
    totalWords = 0
    start = content.find("<p>")
    while start > 0:  # getting all data in every paragraph tag
        end = content.find("</p>", start)
        words = content[start + 3: end]  # getting array of all words between start and end indices
        words = words.strip("\n").split()

        for i in words:  # looping through the array of words
            if i not in pageDict:  # adding the word to the dictionary with a count that increments
                pageDict[i] = 0
            pageDict[i] += 1

        totalWords += len(words)  # getting the total amount of words in the paragraph tag
        start = content.find("<p>", end)  # finding the beginning of the next paragraph tag

    return {"Page Dictionary" : pageDict, "Total Words": totalWords}

def write_term_frequency(title, pageDict, totalWords, websiteName):
    freqFilePath = os.path.join("pageFreqFiles", title + "TF.json")
    TFDict = {}

    for i in pageDict:
        if type(pageDict[i]) is int:
            TFDict[i + "TF"] = pageDict[i] / totalWords

    TFDict["URL"] = websiteName + title + '.html'
    TFDict["Title"] = title

    with open(freqFilePath, "w") as fp:
        json.dump(TFDict, fp)
    fp.close()

def get_links(content, title, websiteName):
    links =[]

    outLinks = content[content.find("<a"): content.rfind('</a>') + len("</a>")]                                                                                                                                                                                                                                                                                                                                                 #https://www.youtube.com/watch?v=8oQ8zbyCJd0&ab_channel=BugHorseInternational
    linkStart = outLinks.find("href=\"")

    while linkStart != -1:
        endLink = outLinks.find("\">", linkStart)
        link = outLinks[linkStart + len("href=\""): endLink]

        if link[0] != ".":
            websiteName = link[:link.rfind("/") + 1]
        else:
            link = link[2:]

        links.append(websiteName + link)
        addIncoming(websiteName + title + '.html', link[:link.index(".")])
        linkStart = outLinks.find("href=\"", endLink)

    return links

def get_text(content, websiteName):
    global totalPages
    totalPages += 1

    titleStart = content.find("<title")
    title = content[content.find(">", titleStart) + 1: content.find("<", titleStart + 1)]

    pageInfo = get_wordCount(content)
    pageDict = pageInfo["Page Dictionary"]  # dictionary that hold's a page's important values
    totalWords = pageInfo["Total Words"]  # getting total words

    write_term_frequency(title, pageDict, totalWords, websiteName)

    pageDict["Title"] = title
    pageDict["URL"] = websiteName + title + '.html'
    pageDict["Total Words"] = totalWords
    pageDict['outgoingLinks'] = get_links(content, title, websiteName)

    filePath = os.path.join("pageFiles", title + ".json")
    with open(filePath, "w") as fp:
        json.dump(pageDict, fp)
    fp.close()

    return pageDict["outgoingLinks"]


def addIncoming(addLink, link):
    fHand = open(os.path.join("incomingLinks", link + ".txt"), "a")
    fHand.write(addLink + " ")
    fHand.close()


def get_IDF_Data():
    global totalPages
    itemPages = {}
    for i in os.listdir("pageFiles"):
        fHand = open(os.path.join("pageFiles", i))
        data = json.load(fHand)
        fHand.close()
        for i in data:
            if i == "Title":
                break
            if i not in itemPages:
                itemPages[i] = 0
            itemPages[i] += 1

    idfData = {}
    for i in itemPages:
        idfData[i + "IDF"] = math.log(totalPages / (1 + itemPages[i]), 2)
    return idfData

def get_TFIDF_Data():
    idfData = get_IDF_Data()
    for i in os.listdir("pageFreqFiles"):
        fHand = open(os.path.join("pageFreqFiles", i))
        tfData = json.load(fHand)
        fHand.close()

        moretfData = {}
        for k in tfData:
            if k == "URL":
                break
            moretfData[k + "IDF"] = math.log(1 + tfData[k], 2) * idfData[k.strip("TF") + "IDF"]

        tfData.update(moretfData)
        with open(os.path.join("pageFreqFiles", i), "w") as fp:
            json.dump(tfData, fp)
        fp.close()

    with open(os.path.join("pageFreqFiles", "IDFData.json"), "w") as fp:
        json.dump(idfData, fp)
    fp.close()

def crawl(seed):
    import time
    global totalPages

    clear_Data()
    start = time.time()

    outgoingLinks = [seed]

    allPages[seed] =0

    while len(outgoingLinks) > 0:
        page = outgoingLinks[0]
        allPages[page] = 0
        websiteName = page[:page.rfind("/") + 1]

        newLinks = get_text(webdev.read_url(page), websiteName)

        for i in newLinks:
            if i not in allPages:
                allPages[i] = 0
                outgoingLinks.append(i)

        outgoingLinks.pop(0)

    get_TFIDF_Data()
    pageRank.pageRank()

    end = time.time()
    #print(end - start)
    return totalPages
