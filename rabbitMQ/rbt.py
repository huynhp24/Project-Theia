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
# from serverside import labels, textdetect
import json, time
import mysql.connector
import configparser
from os import path
import logging
from logging.handlers import RotatingFileHandler


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

        filestamp = time.strftime('%Y-%m-%d-%I:%M')
        with open('label.json', 'r') as f:
            labelResult = json.load(f)

        labelJson = json.dumps(labelResult)

        with open('imgText.json', 'r') as f:
            textResult = json.load(f)
        # make json file from dict to string
        textJson = json.dumps(textResult)

        sen = Nat_Lang_Gen.Run(labelResult, textResult)
        audio_file, translate_text = translate.textToSpeech(sen, id, lan)

        l.info("Incoming url " + str(audio_file))

        tsql = "insert into jsondata(uuid, image_Location, label_list, detect_text, sentence, audio_Location, file_date) values (%s, %s, %s, %s, %s, %s, %s)"
        cur.execute(tsql, (id, url, labelJson, textJson, translate_text, audio_file, filestamp))
        l.info('Storing into database: ' + str(id) + ', ' + str(url) + ', ' + str(translate_text) + ', ' + str(audio_file ))
        conn.commit()
        # removing the image file on server once uploads to S3 bucket, so it won't overload the server
        os.remove("/opt/theia/rabbitMQ/" + imgFile)

    else:
        l.error("Database connection unsuccesful.")

    cur.close()
    conn.close()


def imgPathToS3(imgPath, uuid, lan):
    imgFile = os.path.basename(imgPath)
    print('--------')
    path = os.path.join(SOURCEDIR, imgFile)
    l.info('Joining the path for img upload to rabbitMQ dir: ' + path)
    with open(imgPath, "rb") as f:
        s3.upload_fileobj(f, S3PATH, imgFile)
        l.info('Had successfully upload ' + imgPath + " to s3 bucket : " + S3PATH)
    textInImage = textdetect.detect_text(imgFile, S3PATH)
    labelResult = labels.detect_labels(imgFile, S3PATH)

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
        # Warning this is not a image file. Please double check. Only accept .png and .jpg and .jpeg
        l.warning(" Not image file. Double check")
    else:
        webpage = urlopen(req).read()
        # this if statement is to strip any string after url format (.jpg/.png/ .jpeg)
        if (img.find('.png') or img.find('.jpg') or img.find('.jpeg')):
            # this function make the url as a list
            url = re.findall(r'(?:http\:|https\:)?\/\/.*\.(?:png|jpg|jpeg)', img)

            imURL = ''.join(url)
            imgFile = os.path.basename(imURL)
            with open(imgFile, 'wb') as f:
                f.write(webpage)
            imgurl = Image.open(imgFile)
            imgurl.close()
            l.info(" The URL provided is an image: " + imgFile)
            imgPathToS3(imgFile, uuid, lan)

        else:
            l.error(" Not an image file. Only accpet URL ends with .png or .jpg or .jpeg")



def receive(rmq_q):
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            channel = connection.channel()
            channel.queue_declare(queue=rmq_q)

            def callback(ch, method, properties, body):
                img = body.decode("utf-8")
                l.info(rmq_q)
                # convert string to dictionary
                res = json.loads(img)
                imgname = res['msg']
                uuid = res['uuid']
                lan = res['language']
                l.info(" receiving UUID : " + uuid)
                l.info(" receiving language : " + lan)
                l.info(" Incoming msg: " + imgname + " sending from " + rmq_q)
                if (rmq_q == 'image_url'):
                    checkingImgURL(imgname, uuid, lan)
                else:
                    l.info('imagePath')
                    imgPathToS3(imgname, uuid, lan)
                l.info('*******************')

            channel.basic_consume(queue=rmq_q, on_message_callback=callback, auto_ack=True)
            l.info('[*] Waiting for messages in the ' + rmq_q + ' queue. To exit press CTRL+C')
            channel.start_consuming()
        except:
            l.exception("Consumer for: " + rmq_q + " died unexpectedly. Restarting in 5 seconds...")
            time.sleep(5)

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
