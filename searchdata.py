import json
import math
import os


def get_page():
    return
def checkURL(pageName):
    if os.path.join("pageFiles", pageName + ".json"):
        return True
    return False

def get_Links(URL, inout):
    page = URL.strip("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/").strip(".html") + ".json"
    if checkURL(page):
        fHand = open(os.path.join("pageFiles", page))
        data = json.load(fHand)
        fHand.close()

        if len(data) == 0:
            return None
        return data[inout]
    return None

def get_outgoing_links(URL):
    return get_Links(URL, "outgoinglinks")

def get_incoming_links(URL):
    return get_Links(URL, "incominglinks")

def get_page_rank(URL):
#returns pageRank value of the URL page
    #if the url was not found during crawl, return -1
    #BRUHHHHHH< read about this more before starting
    return 0
def get_idf(word):
    numWordPages =0
    numPages =0
    files = os.listdir("pageFiles")

    for i in files:
        fHand = open(os.path.join("pageFiles", i))
        data = json.load(fHand)
        fHand.close()
        if word in data:
            numWordPages +=1
        numPages +=1

    if numWordPages == 0:
        return 0
    return math.log((numPages/(1+numWordPages)), 2)

def get_tf(URL, word):
    page = URL.strip("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/").strip(".html") + ".json"

    if checkURL(page):

        fHand = open(os.path.join("pageFiles", page))
        data = json.load(fHand)
        fHand.close()
        if word in data:
            return data[word] / data["Total Words"]
        return -1
    return -1


def get_if_idf(URL, word):
#return the tf-idf weight of the word within URL
    # see formula on instructions page
    return 0

print(get_idf("blueberry"))
