import time
import ParseData as Pd
import WebScrape as Ws


badCalls = 0
titleNumber = 0
providerList = ['', 'hulu/', 'disney-plus/', 'hbo-max/', 'amazon-prime-video/']  # '' means netflix
badAPIcalls = []


def mainFunc():
    provider = ""  # starts with netflix
    pageNumber = 0  # Should start with 0

    start = time.time()
    Ws.loopThroughScrapePages(provider, pageNumber)
    Pd.writeToJson(badAPIcalls)
    end = time.time()
    print('total time: ' + str(end - start) + ' seconds.')
    print("BAD calls " + str(badCalls))


if __name__ == '__main__':
    mainFunc()
