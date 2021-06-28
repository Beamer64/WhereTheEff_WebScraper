import json
import traceback
import SetData


def parseAPIresults(APIresults, title, titleType):
    badChars = ["'"]

    if titleType == "tv":
        key = 'name'
    else:
        key = 'title'

    try:
        if SetData.containsAny(title, badChars) == 1:
            for c in badChars:
                title = title.replace(c, '')
            print(title)

        resultsDict = parseDictData(APIresults, "results")
        if len(resultsDict) > 0:
            for item in resultsDict:
                resultsDict = item

                keyVal = parseDictData(resultsDict, key)
                if keyVal == title:
                    break

        return resultsDict
    except Exception:
        traceback.print_exc()
        print("parseAPIresults() Catch")


def parseDictData(dictionary, key):
    value = {}  # empty dictionary
    try:
        if len(dictionary) > 0:
            for k, v in dictionary.items():
                if k == key:
                    if v is not None:
                        value = v
                    return value
        return value
    except Exception:
        traceback.print_exc()
        print("parseDictData() Catch")


# writes the results of the scrape to a json for viewing
def writeToJson(d):
    try:
        with open('Title_Results/results.json', 'w') as outfile:
            json.dump(d, outfile)
    except Exception:
        traceback.print_exc()
        print("writeToJson() Catch")


# Returns Config value based on config variable name
def getFromConfig(config, configValue):
    try:
        with open("config.json") as json_data_file:
            configData = json.load(json_data_file)

        return configData[config][configValue]
    except Exception:
        traceback.print_exc()
        print("getFromConfig() Catch")
