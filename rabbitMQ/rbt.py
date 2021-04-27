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
sys.path.insert(1,'/opt/theia/serverside')
import labels, textdetect, Nat_Lang_Gen, translate
    # Nat_Lang_Gen
# from serverside import labels, textdetect
import json, time
import mysql.connector
import configparser
from os import path
import logging
from logging.handlers import RotatingFileHandler
from s3urls import build_url
from datetime import date, datetime, timedelta

# Reading config file
config = configparser.ConfigParser()
config.read('/opt/theia/config.ini')
config.sections()

try:
    if path.exists(sys.argv[1]):
        config.read(sys.argv[1])
except IndexError:
    if path.exists('/opt/theia/config.ini'):
        config.read('/opt/theia/config.ini')
    elif path.exists('config.ini'):
        config.read('config.ini')
    else:
        print("No config file found")

# DEST = "/home/ubuntu/Project-Theia/rabbitMQ/Images"
# SOURCEDIR = "/home/ubuntu/Project-Theia/rabbitMQ"

# setting up logging
logfile = config['logging']['logdir'] + "/rabbit_py.log"
log_lvl = config['logging']['loglevel']
log_out = config['logging']['log_stream_to_console']


my_handler = RotatingFileHandler(logfile,
                                 mode='a', maxBytes=5 * 1024 * 1024, backupCount=2, encoding=None, delay=0)
my_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(funcName)s (%(lineno)d) %(message)s'))
l = logging.getLogger(__name__)
l.setLevel(log_lvl.upper())
l.addHandler(my_handler)
if log_out.upper() == 'TRUE':
    l.addHandler(logging.StreamHandler())

l.info("Starting backing end processors")

s3 = boto3.client('s3')
S3PATH = config['amazon']['bucket']
REGION = config['amazon']['region']
DEST = config['default']['dest']
SOURCEDIR = config['default']['image_upload_folder']

# Setup Database Connection
db_host = config['database']['host']
db_port = config['database']['port']
db_user = config['database']['user']
db_password = config['database']['password']
db_dbname = config['database']['dbname']


def storeToDB(imgFile, id, lan):
    conn = mysql.connector.connect(user= db_user, password= db_password,
                                   host= db_host,
                                   database= db_dbname)
    cur = conn.cursor()
    # checking if database's connection was successful
    if (conn):
        l.info("Database connection successful")
        url = "https://%s.s3-%s.amazonaws.com/%s" % (S3PATH, REGION, imgFile)
        # print(url)

        # imgS3Location = build_url('bucket-in-path', S3PATH, imgFile, region = 'us-west-1')
        # print(imgS3Location)

        filestamp = time.strftime('%Y-%m-%d-%I:%M')
        with open('label.json', 'r') as f:
            labelResult = json.load(f)

        # audio_file = audio.generate_tts_audio_file(sen,id)
        labelJson = json.dumps(labelResult)

        # l.info(" audio file location: " + audio_file)

        with open('imgText.json', 'r') as f:
            textResult = json.load(f)
        # make json file from dict to string
        textJson = json.dumps(textResult)

        sen = Nat_Lang_Gen.Run(labelResult, textResult)
        audio_file, translate_text = translate.textToSpeech(sen, id, lan)
        # print(type(translate_text))
        # print(translate_text)
        l.info("Incoming url " + str(audio_file))

        tsql = "insert into jsondata(uuid, image_Location, label_list, detect_text, sentence, audio_Location, file_date) values (%s, %s, %s, %s, %s, %s, %s)"
        cur.execute(tsql, (id, url, labelJson, textJson, translate_text, audio_file, filestamp))
        l.info('Storing into database: ' + str(id) + ', ' + str(url) + ', ' + str(translate_text) + ', ' + str(audio_file ))
        conn.commit()

    else:
        l.error("Database connection unsuccesful.")

    cur.close()
    conn.close()

def imgPathToS3(imgPath, uuid, lan):
    imgFile = os.path.basename(imgPath)
    # print(imgFile)
    print('--------')
    path = os.path.join(SOURCEDIR, imgFile)
    l.info('Joining the path for img upload to rabbitMQ dir: ' + path)
    with open(imgFile, "rb") as f:
        s3.upload_fileobj(f, S3PATH, imgFile)
        l.info('Had successfully upload ' + imgPath + " to s3 bucket : " + S3PATH)
    textInImage = textdetect.detect_text(imgFile, S3PATH)
    labelResult = labels.detect_labels(imgFile, S3PATH)
    newpath = os.path.join(DEST, imgFile)
    l.info('Joining the path for img upload to new rabbitMQ Images dir: ' + newpath)
    shutil.move(path, newpath)

    with open('label.json', 'w') as jf:
        json.dump(labelResult, jf)

    with open('imgText.json', 'w') as j:
        json.dump(textInImage, j)

    storeToDB(imgFile, uuid, lan)



def checkingImgURL(img, uuid, lan):
    try:
        req = Request(img, headers={'User-Agent': 'Mozilla/5.0'})  # to unblock server security
        response = requests.get(img)
        l.info(" Responsing url request: " +str(response))
        url = Image.open(BytesIO(response.content))
    except:
        # print(" It is not a image file. Please double check. Only accept .png and .jpg ")
        l.warning(" Not image file. Double check")
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
            l.info(" The URL provided is an image: " + imgFile)
            imgPathToS3(imgFile, uuid, lan)

        else:
            l.error(" Not an image file. Only accpet URL ends with .png or .jpg")


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
        lan = res['language']
        # print(imgname)
        # print(type(imgname))
        # print(uuid)
        l.info(" receiving UUID : " + uuid)
        l.info(" receiving language : " + lan)
        l.info(" Incoming msg: " + imgname + " sending from " + rmq_q)

        if (rmq_q == 'image_url'):
            checkingImgURL(imgname, uuid, lan)

        else:
            print('imagePath')
            imgPathToS3(imgname, uuid, lan)

        print('*******************')


    channel.basic_consume(queue=rmq_q, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages in the ', rmq_q, ' queue. To exit press CTRL+C')
    channel.start_consuming()

def main():
    try:
        l.info("Starting rabbitMQ backend server...")
        # creating thread
        queue = "image_url"
        t1 = threading.Thread(target = receive, args=(queue,))
        t1.start()

        queue = "image_path"
        t2 = threading.Thread(target = receive, args = (queue,))
        t2.start()
        # l.info("Starting thread : " + str(t1) + ", and thread: " +str(t2))
    except:
        l.error("Unable to start thread")

        return False
    else:
        l.info("end")




if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exiting')

        try:
            sys.exit(0)

        except SystemExit:
            os._exit(0)
