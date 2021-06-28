import traceback

import requests
from bs4 import SoupStrainer, BeautifulSoup

import SetData as Sd
import BuildData as Bd
import ParseData as Pd


def loopThroughScrapePages(provider, pageNumber):
    try:
        running = True
        while running:
            fullURL = Bd.buildFullURL(provider, str(pageNumber))  # "" (blank = netflix)
            page = getPageFromURL(fullURL)

            if hasCardTitles(page):
                cardBodies = getCardBodiesFromPage(page)
                if cardBodies:
                    Bd.buildJsonResults(cardBodies, provider)
                    pageNumber += 1
                else:
                    running = False
            else:
                running = False

        Sd.changeProviders(provider)
    except Exception:
        traceback.print_exc()
        print("getAndParseHtmlTitles() Catch")


def hasCardTitles(page):
    cardBodyFilter = SoupStrainer('div', attrs={'class': 'card-body'})
    soupCardBody = BeautifulSoup(page.content, 'lxml', parse_only=cardBodyFilter)
    cardTitles = soupCardBody.find_all('h5', attrs={'class': 'card-title'})

    if cardTitles:
        return True

    return False


def getSeriesIdentifierFromPage(page):
    seriesFilter = SoupStrainer('div', attrs={'class': 'card card-plain information'})
    soupButtonParse = BeautifulSoup(page.content, 'lxml', parse_only=seriesFilter)
    seriesIdentifier = soupButtonParse.find_all('h6', attrs={'class': 'card-category'})

    return seriesIdentifier


def getServiceButtonFromPage(page):
    seriesFilter = SoupStrainer('div', attrs={'class': 'card card-plain information'})
    soupButtonParse = BeautifulSoup(page.content, 'lxml', parse_only=seriesFilter)
    serviceButton = soupButtonParse.find_all('a', attrs={'class': 'btn btn-danger btn-block watch-on-service'})

    return serviceButton


def getPageFromURL(url):
    requests_session = requests.Session()
    return requests_session.get(url)


def getCardBodiesFromPage(page):
    cardBodyFilter = SoupStrainer('div', attrs={'class': 'card-body'})
    soupCardBody = BeautifulSoup(page.content, 'lxml', parse_only=cardBodyFilter)
    return soupCardBody.find_all('div', attrs={'class': 'card-body'})


def getStreamServiceLinkAndType(provider, title):
    streamLink = ""
    baseSiteURL = Pd.getFromConfig("URLs", "baseSiteURL")

    serviceLink = baseSiteURL + provider + 'title/' + title
    page = getPageFromURL(serviceLink)

    serviceButton = getServiceButtonFromPage(page)

    if 'season' in str(getSeriesIdentifierFromPage(page)).lower():
        titleType = 'tv'
    else:
        titleType = 'movie'

    if serviceButton:
        for pt in serviceButton:
            hrefButtonString = str(pt)
            if provider == '':  # Netflix
                try:
                    titleString = hrefButtonString.split('/')[2].lstrip().split('<')[0].rstrip()
                    streamLink = baseSiteURL + 'out/' + titleString
                except Exception:
                    traceback.print_exc()
                    streamLink = 'No Link Available'

            elif provider == 'disney-plus/':
                try:
                    streamLink = hrefButtonString.split('=')[2].lstrip().split(' ')[0].rstrip()
                except Exception:
                    traceback.print_exc()
                    streamLink = 'No Link Available'

            elif provider == 'hulu/':
                try:
                    streamLink = hrefButtonString.split('"')[3].lstrip().split(' ')[0].rstrip()
                except Exception:
                    traceback.print_exc()
                    streamLink = 'No Link Available'

            elif provider == 'hbo-max/':
                try:
                    streamLink = hrefButtonString.split('"')[3].lstrip().split(' ')[0].rstrip()
                except Exception:
                    traceback.print_exc()
                    streamLink = 'No Link Available'

            elif provider == 'amazon-prime-video/':
                try:
                    streamLink = hrefButtonString.split('"')[3].lstrip().split('"')[0].rstrip()
                except Exception:
                    traceback.print_exc()
                    streamLink = 'No Link Available'
            else:
                streamLink = 'No Link Available'

    return streamLink, titleType
