from PIL import Image
from urllib.request import Request, urlopen
import os
import sys
from io import BytesIO
from os.path import splitext, basename
import shutil
import boto3
from serverside import textdetect, runConfig
# import urllib.request
# import requests

s3 = boto3.client('s3')
S3PATH = "bucket-image"

def imgPath(imgPath):
    imgFile = os.path.basename(imgPath)
    print(imgFile)
    print(type(imgFile))
    with open(imgFile, "rb") as f:
        s3.upload_fileobj(f, S3PATH, imgFile)
        print("*** Sucessfully upload " + imgPath + " to s3 bucket : " + S3PATH)
    textdetect.detect_text(imgPath, S3PATH)
    runConfig.detect_labels(imgPath, S3PATH)

def checkURL(imgurl, req):
    try:
        filename = os.path.basename(imgurl)
        print(filename)
        # print(type(filename))
        # webpage = urlopen(req).read()
        # print(type(webpage))
        # webpage = requests.get(req, stream=True, timeout=1)

        # img = Image.open(filename)
        # img.close()
        try:
            if (imgurl.endswith('.png') or imgurl.endswith('.jpg')):
                webpage = urlopen(req).read()
                print("The url ends with .jpg or .png")
        except Exception as e:
            print("Error: ", e)
            return False
        else:
            with open(filename, 'wb') as f:
                f.write(webpage)
    # except IOError:

    except IOError:
        print(" It is not an image file. Please double check. Only accept .png and .jpg")
        sys.exit(0)

    else:

        img = Image.open(filename)
        # for aws to upload it to s3
        buffered = BytesIO()
        img.save(buffered, format=img.format)
        img_str = buffered.getvalue()

        # UPLOAD  TO S3 BUCKET
        s3.upload_fileobj(buffered, S3PATH, filename)
        print("It's a URL image ")

        img.close()
        print(type(filename))
        print(filename)
        textdetect.detect_text(filename, S3PATH)
        imgPath(filename)





imgurl = 'https://pyxis.nymag.com/v1/imgs/99e/6f5/6eed622d1b1b0a77caad3e658d61630b76-baby-yoda.rsquare.w700.jpg'
# imgurl = 'https://i2.wp.com/dailytrojan.com/wp-content/uploads/2020/10/Screen-Shot-2020-10-26-at-9.05.47-PM-1-1030x533.png?resize=1030%2C533&ssl=1'
sourceDir = 'C:/Users/who/PycharmProjects/Project-Theia/serverside/oldPythonFile/'
dest = 'C:/Users/who/PycharmProjects/Project-Theia/serverside/oldPythonFile/Images/'

# print(type(imgurl))
if (imgurl.startswith('http') or imgurl.startswith('https')):
    req = Request(imgurl, headers={'User-Agent': 'Mozilla/5.0'})
    # req = urllib.request.urlopen(imgurl)
    print('true')
    checkURL(imgurl,req)
else:
    print('false')
    imgPath(imgurl)

# disassembled = urlparse(imgurl)
# filename, ext = splitext(basename(disassembled.path))

    # path = os.path.join(sourceDir, filename)
    # newpath = os.path.join(dest, filename)
    # print(path)
    # shutil.move(path, newpath)




#
# # img_str= img_str.decode("utf-8")


# img.show()