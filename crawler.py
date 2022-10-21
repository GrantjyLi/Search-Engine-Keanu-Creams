from sqlite3 import connect
import webdev
import os
import json

allPages = []
def checkFileDir():
    if not os.path.exists("pageFiles"):
        os.makedirs("pageFiles")

def get_text(content, websiteName):
    linkStart = content.find('</p>')
    linkEnd = content.find('</body>', linkStart)

    outLinks = content[linkStart + 5: linkEnd-1]
    outLinks = outLinks.strip(" ").split()
    links = []

    for x in outLinks:
        if x != '<a':
            links.append("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/" + x[8:16])


    start = content.find("<p>")
    filePath = os.path.join("pageFiles", websiteName+".json")

    while start > 0:
        end = content.find("</p>", start)
        words = content[start + 3: end]
        dict = {}
        words = words.strip("\n").split()
        for i in words:
            if i not in dict:
                dict[i] = 0
            dict[i] += 1

        dict["Total Words"] = len(words)
        dict['incominglinks'] = links
        with open(filePath, "w") as fp:
            json.dump(dict, fp)
        start = content.find("<p>", end)


def crawl(seed):
    global allPages
    allPages.append(seed)
    page = webdev.read_url(allPages[-1])
    websiteName = seed[0:len(seed) - len("N-X.html")]
    webpageName = seed.strip(websiteName)
    get_text(webdev.read_url(seed), webpageName)

    length = 0

    while len(allPages) > length:

        start = page.find("href=\"")

        length = len(allPages)

        while start > 0:
            end = page.find(".html", start)
            link = websiteName + page[start + 8:end + 5]

            if not link in allPages:
                print("crawling " + link)

                crawl(link)
            start = page.find("href=\"", end)

def time():
    import time
    start = time.time()
    global allPages
    checkFileDir()
    files = os.listdir("pageFiles")
    for i in files:
        os.remove(os.path.join("pageFiles", i))
    allPages = []
    crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html")
    end = time.time()

    print(end - start)


time()

# returns the number of total pages found in crawl

