import webdev

allPages = []


def get_text(content, URL):
    fName = URL.strip("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/") + ".txt"
    fileHand = open(fName, "w")
    print("writing " + fName)
    start = content.find("<p>")
    while start > 0:
        end = content.find("</p>", start)
        fileHand.write(content[start + 3: end])

        start = content.find("<p>", end)

    fileHand.close()


def crawl(seed):
    global allPages
    allPages.append(seed)
    page = webdev.read_url(allPages[-1])
    get_text(webdev.read_url(seed), seed)

    length = 0
    websiteName = seed[0:len(seed) - len("N-X.html")]

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
    crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html")
    end = time.time()
    print(end - start)


time()

# returns the number of total pages found in crawl

