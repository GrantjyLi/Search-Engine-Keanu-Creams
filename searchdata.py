#produces data required by search engine
#test correctness of the data produced through crawler.py

def get_outgoing_links(URL):
    #returns a list of URLs that "URL" links to
    # all URLs returned should start with http://
    # doesn't have to be sorted
    # returns None if the given URL was not found in the process
