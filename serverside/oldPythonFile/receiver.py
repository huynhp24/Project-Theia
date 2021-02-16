# @author : Yenni Lam
#!/usr/bin/env python
import pika, sys, os
import boto3
from PIL import Image
import urllib
from urllib.request import urlopen
from io import BytesIO
# from urllib.parse import urlparse
from os.path import splitext, basename
import os
import shutil

s3 = boto3.client('s3')
S3PATH = "bucket-image"
DEST = "/home/ylam/Project-Theia/rabbitMQ/Images"
SOURCEDIR = "/home/ylam/Project-Theia/rabbitMQ"

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='uploads')

    # THIS FUNCTION IS FOR A IMAGE FILE INSTEAD OF URL
    # def uploadToS3(img):
    #     with open(img, "rb") as f:
    #         s3.upload_fileobj(f, S3PATH, img)
    #         print("*** Sucessfully upload " + img + " to s3 bucket : " + S3PATH )

    def callback(ch, method, properties, body):
        # s3 = boto3.client('s3')
        # s3path = "bucket-image"
        print(" [x] Received %s" % body)
        img = body.decode("utf-8") #THIS IS TO CONVERT BYTE TO STRING
        print("make file as string " + img)

        '''if the user uploads a image is url '''
        try:

        # if (img.startswith('http') or img.startswith('https')):
            # split url image string to file and extension
            # disassembled = urlparse(img)
            # filename, ext = splitext(basename(disassembled.path))
            # print(filename)
            # concatenating filename and .jpg to make jpg image file
            # imgFile = filename + '.jpg'

            imgFile = os.path.basename(img)
            print(imgFile)
            # req = Request(img, headers={'User-Agent': 'Mozilla/5.0'}) #to unblock server security

            if (img.endswith('.png') or img.endswith('.jpg')):
                with urllib.request.urlopen(img) as url:
                    with open(imgFile, 'wb') as f:
                        f.write(url.read())
            else:
                print("url not image!! ")
                return False

            # open the image webpage and write bytes to a image file (imgFile) that create
            # webpage = urlopen(req).read()
            # with open( imgFile, 'wb') as f:
            #     f.write(webpage)

            # imgurl = Image.open(imgFile)
            # output = BytesIO()
            # imgurl.save(output, format=imgurl.format)
            #
            # output.seek(0)
            # imgurl.close()
        except:
            print(" It is not a image file ")
            raise

        else:
            imgurl = Image.open(imgFile)
            # convert image bytes to string
            output = BytesIO()
            imgurl.save(output, format=imgurl.format)
            img_str = output.getvalue()
            output.seek(0)
            imgurl.close()
            print("Succesfully upload to S3")
            # UPLOAD  TO S3 BUCKET
            # s3.upload_fileobj(output, S3PATH, imgFile)
            # # imgurl.close()
            # path = os.path.join(SOURCEDIR, imgFile)
            # newpath = os.path.join(DEST, imgFile)

            # shutil.move(path, newpath)

        # else:
        #     uploadToS3(img)
            print(" the image is saving s3")
        # print("end")

        # uploadToS3(imgurl)
        # with open(img, "rb") as f:
        #     s3.upload_fileobj(f, s3path, img)
        #     print("***Sucessfully upload " + img + " to s3 bucket : " + s3path )




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
