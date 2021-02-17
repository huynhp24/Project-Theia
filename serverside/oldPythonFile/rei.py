# @author : Yenni Lam
#!/usr/bin/env python
import pika
import sys
#sys.path.insert(1,'/home/ylam/Project-Theia/serverside')
#import runConfig, textdetect
import boto3
from PIL import Image
from urllib.request import Request, urlopen
from io import BytesIO
from urllib.parse import urlparse
import os
import shutil
import urllib.request
import requests

s3 = boto3.client('s3')
S3PATH = "bucket-image"
DEST = "/home/ylam/Project-Theia/rabbitMQ/Images"
SOURCEDIR = "/home/ylam/Project-Theia/rabbitMQ"

# DEST = "/home/ubuntu/Project-Theia/rabbitMQ/Images"
# SOURCEDIR = "/home/ubuntu/Project-Theia/rabbitMQ"

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='uploads')

    # THIS FUNCTION UPLOADS IMAGE TO S3 GIVEN THE IMAGE FILE PATH
    def imgPathToS3(imgPath):
        imgFile = os.path.basename(imgPath)
        print(imgFile)
        # move given image path to rabbitMQ directory in order to upload image file (not path/folder)to s3
        # path = os.path.join(SOURCEDIR, imgFile)
        # shutil.move(imgPath, path)

        with open(imgFile, "rb") as f:
            s3.upload_fileobj(f, S3PATH, imgFile)
            print("*** Sucessfully upload " + imgPath + " to s3 bucket : " + S3PATH )
        # newpath = os.path.join(DEST, imgFile)
        # shutil.move(path, newpath)
        # textdetect.detect_text(imgFile, S3PATH)
        # runConfig.detect_labels(imgFile, S3PATH)

    # THIS FUNCTION IS TRY AND CATCH ERROR OF THE URL, CHECKING THE END OF THE URL IS .JPG OR .PNG
    # IF THE URL ENDS .PNG OR .JPG THEN UPLOAD TO S3
    def checkingImgURL(img, req):
        try:
            imgFile = os.path.basename(img)
            print(imgFile)
            print(type(imgFile))
            # open the image webpage and write bytes to a image file (imgFile) that create
            # webpage = urlopen(req).read()
            # print(type(webpage))

            # with open( imgFile, 'wb') as f:
            #     f.write(webpage)

            # imgurl = Image.open(imgFile)
            response = requests.get(img)
            url = Image.open(BytesIO(response.content))

        except:
            print(" It is not a image file. Please double check. Only accept .png and .jpg ")
            # sys.exit(0)

        else:
            webpage = urlopen(req).read()
            if (img.endswith('.png') or img.endswith('.jpg')):
                with open(imgFile, 'wb') as f:
                    f.write(webpage)
                imgurl = Image.open(imgFile)
                # convert image bytes to string
                output = BytesIO()
                imgurl.save(output, format=imgurl.format)
                # img_str = output.getvalue()
                output.seek(0)
                # UPLOAD  TO S3 BUCKET
                s3.upload_fileobj(output, S3PATH, imgFile)
                imgurl.close()
                print("This is a image url")
            else:
                print(" Not a image file. Only accpet URL ends with .png or .jpg")
                return False

            # path = os.path.join(SOURCEDIR, imgFile)
            # newpath = os.path.join(DEST, imgFile)
            #
            # shutil.move(path, newpath)
            # imgPathToS3(imgFile)

        print("----fin")


    def callback(ch, method, properties, body):
        print(" [x] Received %s" % body)
        img = body.decode("utf-8") #THIS IS TO CONVERT BYTE TO STRING
        # print("make file as string " + img)

        # '''if the user uploads a image is url '''
        if (img.startswith('http') or img.startswith('https')):
            req = Request(img, headers={'User-Agent': 'Mozilla/5.0'})  # to unblock server security
            # req = urllib.request.urlopen(img)
            checkingImgURL(img, req)

        # when the user uploads image
        else:
            imgPathToS3(img)
        print("-----end")




    channel.basic_consume(queue='uploads', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages in the uploads queue. To exit press CTRL+C')
    channel.start_consuming()



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exiting')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

