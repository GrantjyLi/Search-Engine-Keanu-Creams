#produces data required by search engine
#test correctness of the data produced through crawler.py
import json
import math
import os.path

def checkURL(pageName):
    if os.path.join("pageFiles", pageName + ".json"):
        return True
    return False
def get_outgoing_links(URL):

    page = URL.strip("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/")
    page = page.strip(".html") + ".json"
    """
    if checkURL(page):
        fHand = open(os.path.join("pageFiles", page))
        data = json.load(fHand)
        fHand.close()

        if len(data) ==0:
            return None
        return data
    return None
    """
    fHand = open(page)
    data = json.load(fHand)
    fHand.close()

    if len(data["outgoing"]) == 0:
        return None
    return data["outgoing"]

    # all URLs returned should start with http://

def get_incoming_links(URL):

    page = URL.strip("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/")
    page = page.strip(".html") + ".json"
    """
    if checkURL(page):
        fHand = open(os.path.join("pageFiles", page))
        data = json.load(fHand)
        fHand.close()

        if len(data) ==0:
            return None
        return data
    return None
    """
    fHand = open(page)
    data = json.load(fHand)
    fHand.close()

    if len(data["incoming"]) == 0:
        return None
    return data["incoming"]

    # all URLs returned should start with http://
def get_page_rank(URL):
#returns pageRank value of the URL page
    #if the url was not found during crawl, return -1
    #BRUHHHHHH< read about this more before starting
    return 0
def get_idf(word):



#returns the inverse document frequency of that word within crawled pages
    #see formula on instructions page
    #if word was not found in any crawled documents, return 0
    return 0

def get_tf(URL, word):
    page = URL.strip("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/")
    page = page.strip(".html") + ".json"

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

