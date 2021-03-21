import configparser
import boto3
import sys
import os
from os import path
import pika
import time
from threading import Thread
import requests
import imghdr
import logging
from logging.handlers import RotatingFileHandler

# Reading config file
config = configparser.ConfigParser()
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

logfile = config['logging']['logdir'] + "/backend_processors.log"
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

l.info("Starting theia backend processors...")

def rmq_consumer(rmq_queue, dispatch_function):
    while 1:
        try:
            l.info("Starting to consume from " + rmq_queue)

            rmq_server = config['rabbitmq']['rmq_server']
            rmq_port = config['rabbitmq']['rmq_port']
            rmq_user = config['rabbitmq']['rmq_username']
            rmq_pass = config['rabbitmq']['rmq_password']
            rmq_credentials = pika.PlainCredentials(rmq_user, rmq_pass)
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=rmq_server,
                                                                           port=rmq_port,
                                                                           credentials=rmq_credentials))
            channel = connection.channel()
            channel.queue_declare(queue=rmq_queue)

            def callback(ch, method, properties, body):
                string = body.decode("utf-8")
                l.info(" [x] Received %r" % string + " from queue: " + rmq_queue)
                dispatch_function(body=string)

            channel.basic_consume(queue=rmq_queue, on_message_callback=callback, auto_ack=True)
            channel.start_consuming()
        except:
            l.exception("RMQ Consumer for queue: " + rmq_queue + " died unexpectedly. Restarting in 3 seconds")
            time.sleep(3)


def process_url_download_image(body, image_upload_folder):
    l.info("Downloading image: " + str(body) + " to " + image_upload_folder)
    try:
        filename = os.path.basename(body)
        response = requests.get(body)
        file = open(image_upload_folder + "/" + filename, "wb")
        file.write(response.content)
        file.close()
        return image_upload_folder + "/" + filename
    except:
        l.exception("Invalid URL")


def process_url(body):
    image_upload_folder = config['default']['image_upload_folder']
    image_allowed_file_extensions = config['default']['image_allowed_file_extensions']
    image_file = process_url_download_image(body, image_upload_folder)
    if image_file is not None:
        image_file_type = imghdr.what(image_file)
        if image_file_type == "jpeg" or image_file_type == "png":
            l.info(image_file + " is " + image_file_type + ". Uploading to s3")
            s3_path = upload_image_to_s3(file=image_file)
            if s3_path is not None:
                l.info("Run Rekonect")
            else:
                l.error("S3 upload returned no valid response")
        else:
            l.error("Unable to upload to S3")
    else:
        l.error("Invalid URL")


def process_image_file(body):
    file = body
    l.info("Processing image file: " + str(file))
    s3_filename = upload_image_to_s3(file)
    l.info(s3_filename)


def upload_image_to_s3(file):
    s3Bucket = config['amazon']['s3Bucket']
    AWS_ACCESS_KEY_ID = config['amazon']['accessKey']
    AWS_SECRET_ACCESS_KEY = config['amazon']['secretKey']
    region = config['amazon']['region']
    s3 = boto3.client(service_name='s3',
                        region_name=region,
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    filename = os.path.basename(file)
    try:
        response = s3.upload_file(file, s3Bucket, filename)
        l.info(str(response))
        l.info("Deleting from local FS: " + file)
        os.remove(file)
        return filename
    except:
        l.exception("Upload to S3 failed")
        return None


if __name__ == '__main__':
    try:
        rmq_queue = "image_url"
        dispatch_function = process_url
        t1 = Thread(target=rmq_consumer, args=(rmq_queue, dispatch_function))
        t1.start()

        rmq_queue = "image_path"
        dispatch_function = process_image_file
        t2 = Thread(target=rmq_consumer, args=(rmq_queue, dispatch_function))
        t2.start()
    except:
        l.exception("Unable to start threads")
        raise
