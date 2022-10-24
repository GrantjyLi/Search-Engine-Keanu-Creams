import json
import os

def get_page(URL):
    return URL[URL.rfind("/")+1:len(URL)-len(".html")] + ".json"

def checkURL(URL):
    filePath = os.path.join("pageFiles", get_page(URL))
    if os.path.isfile(filePath):
        return True
    return False

def get_Links(URL, suffix):
    if checkURL(URL):
        page = get_page(URL)
        fHand = open(os.path.join("pageFiles", page))
        data = json.load(fHand)
        fHand.close()

        if len(data) == 0:
            return None
        return data[suffix]
    return None

def get_outgoing_links(URL):
    return get_Links(URL, "outgoingLinks")

def get_incoming_links(URL):
    return get_Links(URL, "incomingLinks")

def get_page_rank(URL):
    filePath = os.path.join("pageRank", 'data.json')
    if os.path.isfile(filePath):
        data=json.load(open(filePath))
        if URL in data:
            return data[URL]
        return -1

def get_idf(word):
    fHand = open(os.path.join("pageFreqFiles", "IDFData.json"))
    data = json.load(fHand)
    fHand.close()

    if word not in data:
        return 0
    return data[word + "IDF"]

def get_tf_data(URL, word, suffix):

    if checkURL(URL):
        fhand = open(os.path.join("pageFreqFiles", get_page(URL) + "TF"))
        data = json.load(fhand)
        fhand.close()
        return data[word + suffix]
    return 0

def get_tf(URL, word):
    return get_tf_data(URL, word, "TF")
def get_tf_idf(URL, word):
    return get_tf_data(URL, word, "TFIDF")

