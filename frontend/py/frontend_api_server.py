#!flask/bin/python
from flask import Flask, jsonify, render_template, request, Response, \
    redirect, url_for, session, flash, send_from_directory, abort
from flask_cors import CORS, cross_origin
import pika
from werkzeug.utils import secure_filename
import os
import time

#File upload parameters
UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'png', 'jpg'}

# Flask app setup
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.update(SECRET_KEY=os.urandom(24))
#cors = CORS(app, resources={r"/theia/api/v1.0/img_path": {"origins": "*"}})
#app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

# Setup Flask api route
api_route = "/theia/api/v1.0/img_url"
api_route_file = "/theia/api/v1.0/img_path"

# Setup RabbitMQ Connection
rmq_server = ""
rmq_port = 5672
rmq_credentials=pika.PlainCredentials('', '')
rmq_url_image_q = "image_url"
rmq_image_upload_q = "image_path"


def send_rabbitmq(rmq_queue,msg):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rmq_server,
                                                                   port=rmq_port,
                                                                   credentials=rmq_credentials))
    channel = connection.channel()
    channel.queue_declare(queue=rmq_queue)
    channel.basic_publish(exchange='', routing_key=rmq_queue, body=msg)
    print(" [RMQ] Sent: " + msg)
    connection.close()


@app.route(api_route, methods=['POST']) # The sendURL post request
def send_image_url():
    img_url = str(request.data.decode())
    send_rabbitmq(rmq_queue=rmq_url_image_q, msg=img_url)
    return (request.data)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route(api_route_file, methods=['GET', 'POST'])
# @cross_origin(origin='*', headers=['Content-Type', 'multipart/form-data'])
def upload_file():
    # print("1")
    # print(request)
    # print(request.method)
    if request.method == 'POST':
        print("2")
        # check if the post request has the file part
        print("files: " + str(request.files))
        if 'file' not in request.files:
            # print("3")
            flash('No file part')
            return redirect(request.url)
        # print("3.5")
        file = request.files['file']
        # print("4")
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            # print("5")
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # print("6")
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_location = UPLOAD_FOLDER + "/" + filename
            # print(image_location)
            send_rabbitmq(rmq_queue=rmq_image_upload_q, msg=image_location)
            # return(request.args)
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # print("7")
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    while 1:
        try:
            app.run(debug=True)

        except Exception:
            print("Unable to continue the API server, Retrying in 10 seconds")
            time.sleep(10)
