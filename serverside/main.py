from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

import label
import rdsConnect
#import getImage
#import image_helper
#import textractOrder
from NatLangGen import Nat_Lang_Gen

app = Flask(__name__)
api = Api(app)

global labels

"""
This class, rekog, is the endpoint in which S3 image analysis is submitted to Amazon Rekognition and stored in the labels global variable
"""
class rekog(Resource):
    def get(self):
        photo='artworks.jpg'
        bucket='bucket-image'
        global labels
        labels = label.detect_labels(photo,bucket)
    def post(self):
        parser = reqparse.RequestParser()
        
        parser.add_argument('bucket', required=True)
        parser.add_argument('photo', required=True)
        
        args = parser.parse_args()

        photo=args['bucket']
        bucket=args['photo']

        global labels
        labels = label.detect_labels(photo,bucket)
    pass


class natLangGen(Resource):
    def get(self):
        head, sum = Nat_Lang_Gen.RunTest()
        return {'title': head, 'summary':sum}
    def post(self):
        head, sum = Nat_Lang_Gen.RunFull(labels)
        return {'title': head, 'summary':sum}
    pass

"""
This is the end to end s3->rekognition->summarize process
"""
class fullProcess(Resource):
    def post(self):
        #already uploaded to s3

        #Run Amazon Rekognition
        parser = reqparse.RequestParser()
        
        parser.add_argument('bucket', required=True)
        parser.add_argument('photo', required=True)
        
        args = parser.parse_args()

        photo=args['bucket']
        bucket=args['photo']

        global labels
        labels = label.detect_labels(photo,bucket)

        #Run Nat Lang Gen
        head, sum = Nat_Lang_Gen.RunFull(labels)

        return {'title': head, 'summary':sum}

"""
This is the RDS connector object
"""
class rdsConnector(Resource):
    def get():
        rdsConnect.insertTest()

api.add_resource(rekog, '/rekog')
api.add_resource(natLangGen, '/analyzer')
api.add_resource(fullProcess, '/fullJob')


if __name__ == '__main__':
    app.run()  # run our Flask app