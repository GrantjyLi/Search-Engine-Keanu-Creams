import webdev

def crawl(seed):
    pages =[seed]
    length =0
    websiteName = seed[0:len(seed)-len("N-0.html")]
    
    while len(pages) > length:
        page = webdev.read_url(pages[-1])
        start = page.find("href=\"")

        length = len(pages)

        while start > 0:
            end = page.find(".html", start)
            link = websiteName+page[start+8:end+5]

            if not link in pages:
                pages.append(link)

            start = page.find("href=\"",end)
    for i in pages:
        print(i)
    return len(pages)
    
    

crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html")

# reset any existing data
# parse all pages that are in the seed website
# parses through all pages only once
# returns the number of total pages found in crawl

