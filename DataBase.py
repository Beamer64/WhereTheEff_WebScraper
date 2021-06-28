import traceback
import boto3

import main as M
import ParseData as Pd

from boto3.dynamodb.conditions import Attr
from termcolor import colored


def insertIntoDB(newID, title, year, service, link, posterURL, plot, tmdbID):
    try:
        if plot != '' or tmdbID != '':
            print("")
            # table.put_item(
            #     Item={
            #         "id": str(newID),
            #         "tmdbID": tmdbID,
            #         "title": title,
            #         "year": year,
            #         "service": service,
            #         "stream_link": link,
            #         "plot": plot,
            #         "poster_URL": posterURL,
            #         "updated": str(today)
            #     }
            # )
        else:
            M.badCalls += 1
            print(colored("BAD CALL", "red"))
            print("")
            M.badAPIcalls.append({
                "id": str(newID),
                "title": title,
                "year": year,
                "service": service,
                "link": link
            },)
    except Exception:
        traceback.print_exc()
        print("insertIntoDB() Catch")


def exists(title, year):
    aws_access_key_id = Pd.getFromConfig("DynamoDB", "aws_access_key_id")
    aws_secret_access_key = Pd.getFromConfig("DynamoDB", "aws_secret_access_key")
    region = Pd.getFromConfig("DynamoDB", "region")
    endpoint_url = Pd.getFromConfig("DynamoDB", "endpoint_url")

    dynamo = boto3.resource('dynamodb', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region, endpoint_url=endpoint_url)
    tableName = 'where-the-eff-dynamodb-table'
    table = dynamo.Table(tableName)
    retVal = False

    try:
        item = table.scan(
            FilterExpression=Attr('title').eq(title) & Attr('year').eq(year)
        )
    except Exception:
        traceback.print_exc()
        print("insertIntoDB() Catch")
        item = None

    count = item.get('Count')
    if count > 0:
        retVal = True
        print('Title: ' + title + ' (' + year + ')' + ' already exists in the DB.')
    return retVal
