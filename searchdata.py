#produces data required by search engine
#test correctness of the data produced through crawler.py
import math
def get_outgoing_links(URL):
    #returns a list of URLs that "URL" links to
    # all URLs returned should start with http://
    # doesn't have to be sorted
    # returns None if the given URL was not found in the process

def get_incoming_lines(URL):
    #returns a list of URLs that go to URL
    # all URLs returned should start with http://
    # doesn't have to be sorted
    # returns None if the given URL was not found in the process

def get_page_rank(URL):
    #returns pageRank value of the URL page
    #if the url was not found during crawl, return -1
    #BRUHHHHHH< read about this more before starting

def get_idf(word):
    #returns the inverse document frequency of that word within crawled pages
    #see formula on instructions page
    #if word was not found in any crawled documents, return 0

def get_tf(URL, word):
    #returns the term frequency of the word within the given URL page
    #see formula on instructions page
    #if the URL is not found, or the word doesn't exist on the page, then return 0

def get_if_idf(URL, word):
    #return the tf-idf weight of the word within URL
    # see formula on instructions page

