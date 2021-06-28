import json
import traceback

import SetData as Sd


def parseAPIresults(APIresults, title, titleType):
    badChars = ["'"]
    bFoundResults = False

    if titleType == "tv":
        key = 'name'
    else:
        key = 'title'

    try:
        if Sd.containsAny(title, badChars) == 1:
            for c in badChars:
                title = title.replace(c, '')
            print(title)

        resultsDict = parseDictData(APIresults, "results")
        if len(resultsDict) > 0:
            for item in resultsDict:
                resultsDict = item
                for k, v in resultsDict.items():
                    if k == key and v == title:
                        bFoundResults = True

            if not bFoundResults:
                return resultsDict
            else:
                return resultsDict
        else:
            # print("parseAPIresults() Catch")
            return resultsDict
    except Exception:
        traceback.print_exc()
        print("parseAPIresults() Catch")


def parseJsonData(APIresults, key):
    value = ''
    try:
        for k, v in APIresults.items():
            if k == key:
                if v is not None:
                    value = v
                break
    except Exception:
        traceback.print_exc()
        print("parseJsonData() Catch")
    return value


def parseDictData(dictionary, key):
    value = {}  # empty dictionary
    try:
        for k, v in dictionary.items():
            if k == key:
                if v:
                    value = v
                return value
        return value
    except Exception:
        traceback.print_exc()
        print("parseDictData() Catch")


def writeToJson(d):
    try:
        with open('Title_Results/results.json', 'w') as outfile:
            json.dump(d, outfile)
    except Exception:
        traceback.print_exc()
        print("writeToJson() Catch")


def getFromConfig(config, configValue):
    try:
        with open("config.json") as json_data_file:
            configData = json.load(json_data_file)

        return configData[config][configValue]
    except Exception:
        traceback.print_exc()
        print("getFromConfig() Catch")
