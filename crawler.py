import webdev
allPages =[]
def crawl(seed):

    global allPages
    pages =[seed]
    length = 0
    websiteName = seed[0:len(seed)-len("N-X.html")]

    while len(pages) > length:
        page = webdev.read_url(pages[-1])
        start = page.find("href=\"")

        length = len(pages)

        while start > 0:
            end = page.find(".html", start)
            link = websiteName+page[start+8:end+5]

            if not link in allPages:
                print(f"crawling {link}")
                allPages.append(link)
                crawl(link)

            start = page.find("href=\"",end)
    
crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html")

for i in allPages:
    print(i)


# reset any existing data
# parse all pages that are in the seed website
# parses through all pages only once
# returns the number of total pages found in crawl

