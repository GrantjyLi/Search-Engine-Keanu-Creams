import json
import os

from pageRank import pageRank

#Global Variables
idfData = {}
pageRankData = {}

def fetchPageRank():
    global pageRankData
    filePath = os.path.join("pageRank", 'data.json')
    if os.path.isfile(filePath):
        pageRankData=json.load(open(filePath))
        return
    return -1
    

def fetchIDFData():
    global idfData
    filePath = os.path.join("pageFreqFiles", "IDFData.json")
    if os.path.isfile(filePath):
        idfData = json.load(open(filePath))
        return
    return -1


def get_page(URL):
    return URL[URL.rfind("/")+1:len(URL)-len(".html")]


def checkURL(URL):
    filePath = os.path.join("pageFiles", get_page(URL) + ".json")
    if os.path.isfile(filePath):
        return True
    return False

def get_outgoing_links(URL):
    if checkURL(URL):
        page = get_page(URL) + ".json"
        fHand = open(os.path.join("pageFiles", page))
        data = json.load(fHand)
        fHand.close()

        if len(data) == 0:
            return None
        return data["outgoingLinks"]
    return None


def get_incoming_links(URL):
    if checkURL(URL):
        fHand = open(os.path.join("incomingLinks", get_page(URL)) + ".txt")
        list = fHand.read().split()
        fHand.close()
        return list
    return None
def get_page_rank(URL):
    global pageRankData
    if pageRankData == {}:
        fetchPageRank()
    if URL in pageRankData:
        return pageRankData[URL]
    return -1


def get_idf(word):
    global idfData
    if idfData == {}:
        fetchIDFData()
    if word + "IDF" not in idfData:
        return 0
    return idfData[word + "IDF"]


def get_tf_data(URL, word, suffix):
    if checkURL(URL):
        fhand = open(os.path.join("pageFreqFiles", get_page(URL) + "TF" + ".json"))
        data = json.load(fhand)
        fhand.close()

        if word + suffix not in data:
            return 0
        return data[word + suffix]
    return 0

def get_tf(URL, word):
    return get_tf_data(URL, word, "TF")

def get_tf_idf(URL, word):
    return get_tf_data(URL, word, "TFIDF")


