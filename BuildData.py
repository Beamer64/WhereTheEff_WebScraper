import traceback
import urllib
import uuid
import requests
import datetime
import SetData
import WebScrape
import DataBase
import ParseData

import main as Main


def buildFullURL(provider, pageNumber):
    maxYear = str(datetime.datetime.now().year + 1)
    baseSiteURL = ParseData.getFromConfig("URLs", "baseSiteURL")

    baseURL = baseSiteURL + provider
    retUrl = baseURL + '?min-rating=0&min-year=1920&max-year=' + maxYear + '&order=title&originals=0&page=' + pageNumber
    return retUrl


def buildJsonResults(cardBodies, provider):
    for pt in cardBodies:
        titleName = str(pt)
        try:
            if 'tab-content' in titleName:
                continue
            else:
                stripTitle = titleName.split('>')[3].lstrip().split('<')[0].rstrip()  # Gets the Clean Title. Example: "This Title"
        except Exception:
            traceback.print_exc()
            stripTitle = 'No Title Available'

        try:
            stripYear = titleName.split('>')[6].lstrip().split('<')[0].rstrip()  # Gets the Title Year. Example: "1996"
        except Exception:
            traceback.print_exc()
            stripYear = 'No Year Available'

        # Gets the Title Stream Service Link. Example Link Title: "this-title-name"
        if provider == '':  # Netflix
            try:
                sRawTitle = str(titleName.split('/')[2].lstrip().split('<')[0].rstrip())
                sStreamLink, titleType = WebScrape.getStreamServiceLinkAndType(provider, sRawTitle)
            except Exception:
                traceback.print_exc()
                sStreamLink = 'No Link Available'
                titleType = ""
        elif provider == 'disney-plus/':
            try:
                sRawTitle = str(titleName.split('/')[3].lstrip().split('<')[0].rstrip())
                sStreamLink, titleType = WebScrape.getStreamServiceLinkAndType(provider, sRawTitle)
            except Exception:
                traceback.print_exc()
                sStreamLink = 'No Link Available'
                titleType = ""
        elif provider == 'hulu/':
            try:
                sRawTitle = str(titleName.split('/')[3].lstrip().split('<')[0].rstrip())
                sStreamLink, titleType = WebScrape.getStreamServiceLinkAndType(provider, sRawTitle)
            except Exception:
                traceback.print_exc()
                sStreamLink = 'No Link Available'
                titleType = ""
        elif provider == 'hbo-max/':
            try:
                sRawTitle = str(titleName.split('/')[3].lstrip().split('<')[0].rstrip())
                sStreamLink, titleType = WebScrape.getStreamServiceLinkAndType(provider, sRawTitle)
            except Exception:
                traceback.print_exc()
                sStreamLink = 'No Link Available'
                titleType = ""

        elif provider == 'amazon-prime-video/':
            try:
                sRawTitle = str(titleName.split('/')[3].lstrip().split('<')[0].rstrip())
                sStreamLink, titleType = WebScrape.getStreamServiceLinkAndType(provider, sRawTitle)
            except Exception:
                traceback.print_exc()
                sStreamLink = 'No Link Available'
                titleType = ""
        else:
            sStreamLink = 'No Link Available'
            titleType = ""

        Main.titleNumber += 1
        print(str(Main.titleNumber) + '.) ' + SetData.getProviderNames(provider) + ' - ' + stripTitle)
        if stripTitle != '':
            if stripYear == '':
                stripYear = ' '
            buildDbInsert(stripTitle, stripYear, sStreamLink, provider, titleType)
        else:
            print('Title: ' + stripTitle + ', Year: ' + stripYear + ', Link: ' + sStreamLink + ', Provider: ' + provider)
            print(titleName)
            print(cardBodies)
            print("buildJsonResults() Catch")


def buildDbInsert(title, year, link, provider, titleType):
    service = SetData.getProviderNames(provider)
    newID = uuid.uuid4()
    if DataBase.titleExists(title, year):
        return
    else:
        FullAPIresults = buildAPICall(title, year, titleType)
        dict_parsedAPIforResults = ParseData.parseAPIresults(FullAPIresults, title, titleType)
        str_Plot = ParseData.parseDictData(dict_parsedAPIforResults, "overview")
        str_TmdbID = ParseData.parseDictData(dict_parsedAPIforResults, 'id')
        str_PosterURL = buildPosterURL(dict_parsedAPIforResults)
        DataBase.insertIntoDB(newID, title, year, service, link, str_PosterURL, str_Plot, str_TmdbID)
        # print("buildDbInsert() Catch")


def buildAPICall(title, year, titleType):
    try:
        queryTitle = urllib.parse.quote(title)
        APIkey = ParseData.getFromConfig("API", "APIkey")

        requestURL = 'https://api.themoviedb.org/3/search/' + titleType + '?api_key=' + APIkey + '&query=' + queryTitle + '&year=' + year
        response = requests.get(requestURL)
        APIresults = response.json()
        return APIresults
    except Exception:
        traceback.print_exc()
        print("buildAPICall() Catch")


def buildPosterURL(parsedAPIdict):
    posterURL = ''
    try:
        APIkey = ParseData.getFromConfig("API", "APIkey")

        requestURL = 'https://api.themoviedb.org/3/configuration?api_key=' + APIkey
        response = requests.get(requestURL)
        APIresults = response.json()

        posterDict = ParseData.parseDictData(APIresults, 'images')
        posterBaseURL = ParseData.parseDictData(posterDict, 'base_url')
        posterPath = ParseData.parseDictData(parsedAPIdict, 'poster_path')
        if posterPath == {}:
            posterURL = "Null"
        else:
            posterURL = posterBaseURL + 'original' + posterPath
    except Exception:
        traceback.print_exc()
        print("buildPosterURL() Catch")
    return posterURL
