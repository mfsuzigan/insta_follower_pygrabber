from openpyxl import load_workbook
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from datetime import datetime
from io import BytesIO
from urllib.request import urlopen

def getImage(url):
    image_data = BytesIO(urlopen(url).read())
    return Image(image_data)

filename = "insta_followers_output_{}.xlsx".format(datetime.now().strftime("%y%m%d%H%M%S%f")[: -3])

workbook = Workbook()
sheet = workbook.active

sheet["A1"] = "pk"
sheet["B1"] = "username"
sheet["C1"] = "full_name"
sheet["D1"] = "is_private"
sheet["E1"] = "profile_pic"
sheet["E1"] = "profile_pic_url"

workbook.save(filename=filename)


url = 'https://instagram.fuba2-1.fna.fbcdn.net/v/t51.2885-19/309284379_584430120131402_665952330297638628_n.jpg?stp=dst-jpg_s150x150&_nc_ht=instagram.fuba2-1.fna.fbcdn.net&_nc_cat=102&_nc_ohc=MubAgD_6yYQAX_5NoAj&edm=ALB854YBAAAA&ccb=7-5&oh=00_AfDYedXZlF3wp4NDBHuRCQaCQVpHdwRETXE6ULzuELnlrw&oe=6387E5C7&_nc_sid=04cb80'
url2 = 'https://instagram.fuba2-1.fna.fbcdn.net/v/t51.2885-19/181868110_211938730449739_6172104992184472384_n.jpg?stp=dst-jpg_s150x150&_nc_ht=instagram.fuba2-1.fna.fbcdn.net&_nc_cat=107&_nc_ohc=cM0D7nmiJwMAX-u6yIM&edm=ALB854YBAAAA&ccb=7-5&oh=00_AfA8ILjJ4l72fKwUpXyXHSAHyCL05qyrqBxcx7Q_nTC4kg&oe=6386AB89&_nc_sid=04cb80'

sheet.add_image(getImage(url), "E2")
sheet.add_image(getImage(url2), "E3")

sheet.row_dimensions[2].height = 115
sheet.row_dimensions[3].height = 115
sheet.column_dimensions['E'].width = 16

workbook.save(filename=filename)

