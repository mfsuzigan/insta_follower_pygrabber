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

def getImageFromUrl(url):
    image_data = BytesIO(urlopen(url).read())
    return Image(image_data)

def setupSpreadSheet(sheet):
    sheet["A1"] = "pk"
    sheet["B1"] = "username"
    sheet["C1"] = "full_name"
    sheet["D1"] = "is_private"
    sheet["E1"] = "profile_pic"
    sheet["E1"] = "profile_pic_url"
    
    sheet.column_dimensions['A'].width = GENERAL_WIDTH
    sheet.column_dimensions['B'].width = GENERAL_WIDTH
    sheet.column_dimensions['C'].width = PROFILE_IMAGE_WIDTH
    sheet.column_dimensions['E'].width = PROFILE_IMAGE_WIDTH

def getSpreadSheetName():
    return "insta_followers_output_{}.xlsx".format(datetime.now().strftime("%y%m%d%H%M%S%f")[: -3])

def getFollowers(pk, xIgAppId, cookie):
    headers = {"x-ig-app-id": xIgAppId, "cookie": cookie}
    response = requests.get("https://www.instagram.com/api/v1/friendships/{}/followers/".format(pk), headers=headers)
    
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

def main():
    args = getArgs()

    workbook = Workbook()
    sheet = workbook.active
    setupSpreadSheet(sheet)

    followers = getFollowers(args.pk, args.xIgAppId, args.cookie)

    for index, element in enumerate(followers["users"]):
        rowNumber = index + 2

        sheet["A{}".format(rowNumber)] = element["pk"]
        sheet["B{}".format(rowNumber)] = element["username"]
        sheet["C{}".format(rowNumber)] = element["full_name"]
        sheet["D{}".format(rowNumber)] = element["is_private"]
        sheet["F{}".format(rowNumber)] = element["profile_pic_url"]

        sheet.row_dimensions[rowNumber].height = PROFILE_IMAGE_HEIGHT
        
        sheet.add_image(getImageFromUrl(element["profile_pic_url"]), "E{}".format(rowNumber))

        print("User {} ({}) added".format(str(index + 1), element["username"]))

    workbook.save(filename=getSpreadSheetName())

if __name__ == '__main__':
    main()

