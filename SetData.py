import WebScrape as Ws
import main as M


def changeProviders(currentProvider):
    if currentProvider in M.providerList:
        M.providerList.remove(currentProvider)
        if M.providerList:
            nextProvider = M.providerList[0]
            pageNumber = '0'
            Ws.loopThroughScrapePages(nextProvider, pageNumber)
        else:
            return


def getProviderNames(service):
    if service == '':
        service = 'Netflix'

    elif service == 'disney-plus/':
        service = 'Disney Plus'

    elif service == 'hulu/':
        service = 'Hulu'

    elif service == 'hbo-max/':
        service = 'HBO Max'

    elif service == 'amazon-prime-video/':
        service = 'Amazon Prime'
    return service


def containsAny(sArg, charSet):
    # Check whether sequence str contains ANY of the items in set.
    return 1 in [c in sArg for c in charSet]
