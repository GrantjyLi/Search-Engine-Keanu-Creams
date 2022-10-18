import webdev

def crawl(seed):
    pagesQueue =[seed]
    seedPage = webdev.read_url(seed)
    print(seedPage)

    while pagesQueue[-1] != "":


crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html")
# reset any existing data
# parse all pages that are in the seed website
# parses through all pages only once
# returns the number of total pages found in crawl

