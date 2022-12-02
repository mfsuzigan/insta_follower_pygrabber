from openpyxl import load_workbook
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from datetime import datetime
from io import BytesIO
from urllib.request import urlopen
import requests
import json
import argparse

GENERAL_WIDTH = 18
PROFILE_IMAGE_WIDTH = 16
PROFILE_IMAGE_HEIGHT = 115
INITIAL_FOLLOWERS_REQUEST_MAX_ID = -1

def getImageFromUrl(url):
    image_data = BytesIO(urlopen(url).read())
    return Image(image_data)

def setupSpreadSheet(sheet):
    sheet["A1"] = "pk"
    sheet["B1"] = "username"
    sheet["C1"] = "full_name"
    sheet["D1"] = "is_private"
    sheet["E1"] = "profile_pic"
    sheet["F1"] = "profile_pic_url"
    
    sheet.column_dimensions['A'].width = GENERAL_WIDTH
    sheet.column_dimensions['B'].width = GENERAL_WIDTH
    sheet.column_dimensions['C'].width = GENERAL_WIDTH
    sheet.column_dimensions['E'].width = PROFILE_IMAGE_WIDTH

def getSpreadSheetName():
    return "insta_followers_output_{}.xlsx".format(datetime.now().strftime("%y%m%d%H%M%S%f")[: -3])

def getFollowers(pk, xIgAppId, cookie, nextMaxId):
    headers = {"x-ig-app-id": xIgAppId, "cookie": cookie}
    params = None

    if nextMaxId and not nextMaxId == INITIAL_FOLLOWERS_REQUEST_MAX_ID:
        params = {"next_max_id": nextMaxId}

    response = requests.get("https://www.instagram.com/api/v1/friendships/{}/followers/".format(pk), headers=headers, params=params)
    
    for resp in response.history:
        print(resp.url, resp.text)

    try:
        print(response.text)
        return response.json()
    except ValueError:
        print("Failed getting followers.")

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('pk', help='Target Instagram account ID')
    parser.add_argument('xIgAppId', help='Your Instagram app ID')
    parser.add_argument('cookie', help='Instagram cookie from browser')
    return parser.parse_args()

def writeFollowers(followers, sheet):
    for index, element in enumerate(followers["users"]):
        rowNumber = index + 2

        sheet["A{}".format(rowNumber)] = element["pk"]
        sheet["B{}".format(rowNumber)] = element["username"]
        sheet["C{}".format(rowNumber)] = element["full_name"]
        sheet["D{}".format(rowNumber)] = element["is_private"]
        sheet["F{}".format(rowNumber)] = element["profile_pic_url"]

        sheet.row_dimensions[rowNumber].height = PROFILE_IMAGE_HEIGHT
        profileImage = getImageFromUrl(element["profile_pic_url"])
        sheet.add_image(profileImage, "E{}".format(rowNumber))

        print("Follower {} added to spreadsheet".format(element["username"]))

def main():
    args = getArgs()

    workbook = Workbook()
    sheet = workbook.active
    setupSpreadSheet(sheet)

    shouldGetFollowers = True
    nextMaxId = INITIAL_FOLLOWERS_REQUEST_MAX_ID
    followersCounter = 0

    while shouldGetFollowers:
        followers = getFollowers(args.pk, args.xIgAppId, args.cookie, nextMaxId)
        writeFollowers(followers, sheet)
        followersCounter += len(followers)

        print("Followers added: {}; next_max_id: {}".format(followersCounter, followers["next_max_id"]))

        if "next_max_id" in followers:
            nextMaxId = followers["next_max_id"]

        else:
            break        

    workbook.save(filename=getSpreadSheetName())
    print("\nFinished. Total of {} followers added to spreadsheet.".format(len(followersCounter)))

if __name__ == '__main__':
    main()

