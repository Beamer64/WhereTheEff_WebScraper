import traceback
import urllib
import uuid
import requests
import datetime

import SetData as Sd
import main as M
import WebScrape as Ws
import DataBase as Db
import ParseData as Pd


def buildFullURL(provider, pageNumber):
    maxYear = str(datetime.datetime.now().year + 1)
    baseSiteURL = Pd.getFromConfig("URLs", "baseSiteURL")

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
                sStreamLink, titleType = Ws.getStreamServiceLinkAndType(provider, sRawTitle)
            except Exception:
                traceback.print_exc()
                sStreamLink = 'No Link Available'
                titleType = ""
        elif provider == 'disney-plus/':
            try:
                sRawTitle = str(titleName.split('/')[3].lstrip().split('<')[0].rstrip())
                sStreamLink, titleType = Ws.getStreamServiceLinkAndType(provider, sRawTitle)
            except Exception:
                traceback.print_exc()
                sStreamLink = 'No Link Available'
                titleType = ""
        elif provider == 'hulu/':
            try:
                sRawTitle = str(titleName.split('/')[3].lstrip().split('<')[0].rstrip())
                sStreamLink, titleType = Ws.getStreamServiceLinkAndType(provider, sRawTitle)
            except Exception:
                traceback.print_exc()
                sStreamLink = 'No Link Available'
                titleType = ""
        elif provider == 'hbo-max/':
            try:
                sRawTitle = str(titleName.split('/')[3].lstrip().split('<')[0].rstrip())
                sStreamLink, titleType = Ws.getStreamServiceLinkAndType(provider, sRawTitle)
            except Exception:
                traceback.print_exc()
                sStreamLink = 'No Link Available'
                titleType = ""

        elif provider == 'amazon-prime-video/':
            try:
                sRawTitle = str(titleName.split('/')[3].lstrip().split('<')[0].rstrip())
                sStreamLink, titleType = Ws.getStreamServiceLinkAndType(provider, sRawTitle)
            except Exception:
                traceback.print_exc()
                sStreamLink = 'No Link Available'
                titleType = ""
        else:
            sStreamLink = 'No Link Available'
            titleType = ""

        M.titleNumber += 1
        print(str(M.titleNumber) + '.) ' + Sd.getProviderNames(provider) + ' - ' + stripTitle)
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
    service = Sd.getProviderNames(provider)
    newID = uuid.uuid4()
    if Db.exists(title, year):
        return
    else:
        FullAPIresults = buildAPICall(title, year, titleType)
        dict_parsedAPIforResults = Pd.parseAPIresults(FullAPIresults, title, titleType)
        str_Plot = Pd.parseJsonData(dict_parsedAPIforResults, 'overview')
        str_TmdbID = Pd.parseJsonData(dict_parsedAPIforResults, 'id')
        str_PosterURL = buildPosterURL(dict_parsedAPIforResults)
        Db.insertIntoDB(newID, title, year, service, link, str_PosterURL, str_Plot, str_TmdbID)
        # print("buildDbInsert() Catch")


def buildAPICall(title, year, titleType):
    try:
        queryTitle = urllib.parse.quote(title)
        APIkey = Pd.getFromConfig("API", "APIkey")

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
        APIkey = Pd.getFromConfig("API", "APIkey")

        requestURL = 'https://api.themoviedb.org/3/configuration?api_key=' + APIkey
        response = requests.get(requestURL)
        APIresults = response.json()

        posterDict = Pd.parseJsonData(APIresults, 'images')
        posterBaseURL = Pd.parseJsonData(posterDict, 'base_url')
        posterPath = Pd.parseJsonData(parsedAPIdict, 'poster_path')
        if posterPath == "":
            posterURL = "Null"
        else:
            posterURL = posterBaseURL + 'original' + posterPath
    except Exception:
        traceback.print_exc()
        print("buildPosterURL() Catch")
    return posterURL
