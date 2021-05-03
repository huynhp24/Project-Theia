from configparser import ConfigParser
import boto3
import json

def detect_labels(photo, bucket):
    client = boto3.client('rekognition', 'us-west-1')

    response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
                                    MaxLabels=10)

    print('Detected labels for ' + photo)
    print()
    # result = json.dumps(response)
    return response



