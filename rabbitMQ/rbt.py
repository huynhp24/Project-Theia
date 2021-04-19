import threading
import time
import pika, sys, os
import boto3
from PIL import Image
import urllib.parse
import re
from urllib.request import Request, urlopen
from io import BytesIO
import shutil
import requests
sys.path.insert(1,'/home/ylam/test/serverside')
import labels, textdetect, language
# from serverside import runConfig, textdetect
import json, time
import mysql.connector
from s3urls import build_url
from datetime import date, datetime, timedelta

s3 = boto3.client('s3')
S3PATH = "project-theia-test"
REGION = 'us-west-1'
# DEST = 'C:/Users/who/PycharmProjects/Project-Theia/rabbitMQ/Images'
# SOURCEDIR = 'C:/Users/who/PycharmProjects/Project-Theia/rabbitMQ'
DEST = '/home/ylam/test/rabbitMQ/Images'
SOURCEDIR = '/home/ylam/test/rabbitMQ'
# DEST = "/home/ubuntu/Project-Theia/rabbitMQ/Images"
# SOURCEDIR = "/home/ubuntu/Project-Theia/rabbitMQ"

# def fetchDB(id):
#     conn = mysql.connector.connect(user='ylam', password='ylam',
#                                    host='127.0.0.1',
#                                    database='sys')
#
#     uuid = ''
#     imageLocation =''
#     cur = conn.cursor()
#     sql = "select uuid, image_Location, label_list, detect_text, file_date from jsondata"
#     cur.execute(sql)
#     result = cur.fetchall()
#     for row in result:
#         # if row[0] == id:
#         uuid = row[0]
#         imageLocation = row[1]
#     # print(uuid)
#     # print(imageLocation)
#     # sample = 'uuid: {id}, imageLocation: {lct}'.format(id = uuid, lct = imageLocation)
#     # print(sample)
#     sample_json = '''{{
#                  "uuid": "{id}",
#                  "img_file": "{file}",
#                  "label_list": "things in the picture",
#                  "nat_sentence": "Natural sentence for things in the picture",
#                  "audio_file_location": "https://project-theia-test.s3-us-west-1.amazonaws.com/BeautifulGoblinOSTBeat-Crush-4709474.mp3"
#                }}'''.format(id=uuid, file= imageLocation)
#
#     return sample_json


def storeToDB(imgFile, id):
    conn = mysql.connector.connect(user='ylam', password='ylam',
                                   host='127.0.0.1',
                                   database='sys')
    cur = conn.cursor()
    url = "https://%s.s3-%s.amazonaws.com/%s" %(S3PATH, REGION,imgFile)
    print(url)

    # imgS3Location = build_url('bucket-in-path', S3PATH, imgFile, region = 'us-west-1')
    # print(imgS3Location)

    filestamp = time.strftime('%Y-%m-%d-%I:%M')
    with open('label.json', 'r') as f:
        labelResult = json.load(f)
    # make json file from dict to string
    sen = language.generate_nat_string(labelResult)
    labelJson = json.dumps(labelResult)

    with open('imgText.json', 'r') as f:
        textResult = json.load(f)
    # make json file from dict to string
    textJson = json.dumps(textResult)

    tsql = "insert into jsondata(uuid, image_Location, label_list, detect_text, sentence, file_date) values (%s, %s, %s, %s, %s, %s)"
    cur.execute(tsql, (id, url, labelJson, textJson, sen , filestamp))
    conn.commit()
    # fetchDB(id)
    # sql = "select uuid, image_Location, label_list, detect_text, file_date from jsondata"
    # cur.execute(sql)
    # result = cur.fetchall()
    # for d in result:
    #     print(d)

    cur.close()
    conn.close()

def imgPathToS3(imgPath, uuid):
    imgFile = os.path.basename(imgPath)
    print(imgFile)
    print('--------')
    path = os.path.join(SOURCEDIR, imgFile)

    with open(imgFile, "rb") as f:
        s3.upload_fileobj(f, S3PATH, imgFile)
        print("*** Sucessfully upload " + imgPath + " to s3 bucket : " + S3PATH)
    textInImage = textdetect.detect_text(imgFile, S3PATH)
    labelResult = labels.detect_labels(imgFile, S3PATH)
    newpath = os.path.join(DEST, imgFile)
    shutil.move(path, newpath)

    with open('label.json', 'w') as jf:
        #     json.dump(textInImage, jf)
        json.dump(labelResult, jf)

    with open('imgText.json', 'w') as j:
        json.dump(textInImage, j)

    storeToDB(imgFile, uuid)



def checkingImgURL(img, uuid):
    try:
        req = Request(img, headers={'User-Agent': 'Mozilla/5.0'})  # to unblock server security
        response = requests.get(img)
        url = Image.open(BytesIO(response.content))
    except:
        print(" It is not a image file. Please double check. Only accept .png and .jpg ")
    else:
        webpage = urlopen(req).read()
        # this if statement is to strip any string after url format (.jpg/.png)
        if (img.find('.png') or img.find('.jpg')):
            # this function make the url as a list
            url = re.findall(r'(?:http\:|https\:)?\/\/.*\.(?:png|jpg)', img)
            # print(url)
            imURL = ''.join(url)
            print(imURL)
            imgFile = os.path.basename(imURL)
            with open(imgFile, 'wb') as f:
                f.write(webpage)
            imgurl = Image.open(imgFile)
            imgurl.close()
            imgPathToS3(imgFile, uuid)
            print("This is an image url")

        else:
            print(" Not a image file. Only accpet URL ends with .png or .jpg")


def receive(rmq_q):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue=rmq_q)

    def callback(ch, method, properties, body):
        # print(" [x] Received %r" % body)
        img = body.decode("utf-8")
        print(rmq_q)
        # convert string to dictionary
        res = json.loads(img)
        # print(type(res))
        imgname = res['msg']
        uuid = res['uuid']
        # print(imgname)
        # print(type(imgname))
        # print(uuid)
        if (rmq_q == 'image_url'):
            checkingImgURL(imgname, uuid)

        else:
            print('imagePath')
            imgPathToS3(imgname, uuid)

        print('*******************')


    channel.basic_consume(queue=rmq_q, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages in the ', rmq_q, ' queue. To exit press CTRL+C')
    channel.start_consuming()

def main():
    try:
        # creating thread
        queue = "image_url"
        t1 = threading.Thread(target = receive, args=(queue,))
        t1.start()

        queue = "image_path"
        t2 = threading.Thread(target = receive, args = (queue,))
        t2.start()
    except:
        print("Unable to start thread")
        return False
    else:
        print("end")



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exiting')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
