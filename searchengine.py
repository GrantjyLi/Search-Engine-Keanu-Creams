import crawler
import search


quit = input('Enter E to continue or Q to quit: ')


while quit.lower() != 'q':
    searchQuit = 'e'
    url = input('Enter a url: ')
    crawler.crawl(url)
    while searchQuit.lower() != 'q':
        query = input('Enter a query: ')
        boolean = input("Enter boost value, 1 for true or 0 for false: ")
        if boolean == '1':
            res = search.search(query, True)
        else:
            res = search.search(query, False)
        print(res)

        searchQuit = input('Enter E to search again or Q to quit: ')
    quit = input('Enter E to enter another url or Q to quit: ')