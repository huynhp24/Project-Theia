from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

import label

app = Flask(__name__)
api = Api(app)

def rekog_test():
    photo='artworks.jpg'
    bucket='bucket-image'
    label.detect_labels(photo, bucket)

if __name__ == '__main__':
    app.run()  # run our Flask app