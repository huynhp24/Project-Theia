from configparser import ConfigParser
import boto3
import json

import sys
from os import path
import configparser
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

def detect_labels(photo, bucket):
    REGION = config['amazon']['region']
    client = boto3.client('rekognition', region_name=REGION)

    response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
                                    MaxLabels=10)

    print('Detected labels for ' + photo)
    print()
    # result = json.dumps(response)
    return response



