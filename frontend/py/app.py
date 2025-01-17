#!flask/bin/python
from flask import Flask, jsonify, render_template, request, Response, \
    redirect, url_for, session, flash, send_from_directory, abort
from flask_cors import CORS, cross_origin
import pika
from werkzeug.utils import secure_filename
import os
import time
import configparser
import sys
from os import path
import logging
from logging.handlers import RotatingFileHandler
import uuid
import json
import random
import mysql.connector


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

# Setup logging
logfile = config['logging']['logdir'] + "/front_end_api.log"
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

l.info("Starting theia frontend API server...")


#File upload parameters
UPLOAD_FOLDER = config['default']['image_upload_folder']
ALLOWED_EXTENSIONS = config['default']['image_allowed_file_extensions']

# Flask app setup
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.update(SECRET_KEY=os.urandom(24))
# cors = CORS(app, resources={r"/theia/api/v1.0/img_path": {"origins": "*"}})
# app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

# Setup Flask api route
api_route = config['api_path']['api_route']
api_route_file = config['api_path']['api_route_file']
info_path = config['api_path']['info_path']

# Setup RabbitMQ Connection
rmq_server = config['rabbitmq']['rmq_server']
rmq_port = config['rabbitmq']['rmq_port']
rmq_user = config['rabbitmq']['rmq_username']
rmq_pass = config['rabbitmq']['rmq_password']
rmq_credentials = pika.PlainCredentials(rmq_user, rmq_pass)
rmq_url_image_q = config['rabbitmq']['rmq_url_image_q']
rmq_image_upload_q = config['rabbitmq']['rmq_image_upload_q']


# Setup Database Connection
db_host = config['database']['host']
db_port = config['database']['port']
db_user = config['database']['user']
db_password = config['database']['password']
db_dbname = config['database']['dbname']

def send_rabbitmq(rmq_queue,msg):  # Sends message to rabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rmq_server,
                                                                   port=rmq_port,
                                                                   credentials=rmq_credentials))
    channel = connection.channel()
    channel.queue_declare(queue=rmq_queue)
    channel.basic_publish(exchange='', routing_key=rmq_queue, body=msg)
    l.info(" [RMQ] Sent: " + msg + " to RMQ queue: " + rmq_queue)
    connection.close()


@app.route(api_route, methods=['POST']) # The sendURL post request
def send_image_url():  # What to do if receive URL
    img_url = str(request.data.decode())
    lan = request.headers.get('language')
    l.info("Incoming URL request: " + img_url)
    l.info("Incoming language from image url: " + str(lan))
    new_uuid = str(uuid.uuid4())
    json_data = json.dumps({'msg': img_url, 'uuid': new_uuid, 'language' : lan})
    send_rabbitmq(rmq_queue=rmq_url_image_q, msg=json_data)
    return new_uuid


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route(api_route_file, methods=['GET', 'POST'])
# @cross_origin(origin='*', headers=['Content-Type', 'multipart/form-data'])
def upload_file():  # What to do when it uploads a file
    parameters = '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
    l.info("Incoming request: " + str(request))
    if request.method == 'POST':

        file = request.files['file']
        
        filename = secure_filename(file.filename)
        lan = request.headers.get('language')
        l.info("Incoming language from upload file: " + str(lan))
        l.info("Incoming file: " + filename + " verified. Saving and sending to RMQ")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        image_location = UPLOAD_FOLDER + "/" + filename
        new_uuid = str(uuid.uuid4())
        print(image_location)
        print(new_uuid)

        json_data = json.dumps({'msg': image_location, 'uuid': new_uuid, 'language': lan})

        send_rabbitmq(rmq_queue=rmq_image_upload_q, msg=json_data)
        return new_uuid


@app.route(info_path, methods=['GET'])
def get_data():
    print("HELLO?!")
    img_uuid = request.args.get('uuid')
    print(img_uuid)
    t_uuid = img_uuid.split('?')[0]

    for i in range(1,20):
        try:
            print("Getting data with:" + t_uuid)
            conn = mysql.connector.connect(user= db_user, password= db_password,
                               host= db_host ,
                               database= db_dbname)
            cur = conn.cursor()
            sql = "select uuid, image_Location, label_list, detect_text, sentence, audio_Location, file_date from jsondata where uuid = '" + t_uuid + "'"
            cur.execute(sql)
            result = cur.fetchone()
            uid = result[0]
            imgLocation = result[1]
            sen = result[4]
            audio_Location = result[5]
            print(audio_Location)

            sample_json = '''{"uuid": "''' + uid + '''",
"img_file": "''' + imgLocation + '''",
"nat_sentence": "''' + sen + '''",
"audio_file_location": "''' + audio_Location + '''"}'''
            l.info(sample_json)
            return sample_json
        except:
            l.debug("Waiting for data to be available...")
            time.sleep(1)
    l.error("Data does not exist")
    return "Done"


if __name__ == '__main__':
    while 1:
        try:
            l.info("Starting front end api flask application.")
            app.run(debug=True)

        except Exception:
            l.exception("Unable to continue the API server. Restarting in 3 seconds")
            time.sleep(3)
