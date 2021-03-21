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
#cors = CORS(app, resources={r"/theia/api/v1.0/img_path": {"origins": "*"}})
#app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

# Setup Flask api route
api_route = config['api_path']['api_route']
api_route_file = config['api_path']['api_route_file']
# Setup RabbitMQ Connection
rmq_server = config['rabbitmq']['rmq_server']
rmq_port = config['rabbitmq']['rmq_port']
rmq_user = config['rabbitmq']['rmq_username']
rmq_pass = config['rabbitmq']['rmq_password']
rmq_credentials=pika.PlainCredentials(rmq_user, rmq_pass)
rmq_url_image_q = config['rabbitmq']['rmq_url_image_q']
rmq_image_upload_q = config['rabbitmq']['rmq_image_upload_q']


def send_rabbitmq(rmq_queue,msg):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rmq_server,
                                                                   port=rmq_port,
                                                                   credentials=rmq_credentials))
    channel = connection.channel()
    channel.queue_declare(queue=rmq_queue)
    channel.basic_publish(exchange='', routing_key=rmq_queue, body=msg)
    l.info(" [RMQ] Sent: " + msg + " to RMQ queue: " + rmq_queue)
    connection.close()


@app.route(api_route, methods=['POST']) # The sendURL post request
def send_image_url():
    img_url = str(request.data.decode())
    l.info("Incoming URL request: " + img_url)
    send_rabbitmq(rmq_queue=rmq_url_image_q, msg=img_url)
    new_uuid = str(uuid.uuid4())
    return (new_uuid)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route(api_route_file, methods=['GET', 'POST'])
# @cross_origin(origin='*', headers=['Content-Type', 'multipart/form-data'])
def upload_file():
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
        if 'file' not in request.files:
            l.warning("No file part")
            return FileNotFoundError

        file = request.files['file']
        if file.filename == '':
            l.warning("No file selected")
            return FileNotFoundError

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            l.info("Incoming file: " + filename + " verified. Saving and sending to RMQ")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_location = UPLOAD_FOLDER + "/" + filename
            send_rabbitmq(rmq_queue=rmq_image_upload_q, msg=image_location)
            new_uuid = str(uuid.uuid4())
            return new_uuid
    return parameters


# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     l.info("WTF is this function, i don't get why this is needed but if it's gone things break. idk wtf bbq")
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)


if __name__ == '__main__':
    while 1:
        try:
            l.info("Starting front end api flask application.")
            app.run(debug=True)

        except Exception:
            l.exception("Unable to continue the API server. Restarting in 3 seconds")
            time.sleep(3)
