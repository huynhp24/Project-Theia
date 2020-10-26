
import os
import boto3
from pprint import pprint

#print(os.getcwd())
sourceDir ='/home/ubuntu/images'
file = 'artworks.jpg'
s3 = boto3.resource('s3')
BUCKET = "bucket-image"


#print(os.listdir( sourceDir ))
imageFile = os.listdir(sourceDir)


s3.meta.client.upload_file('/home/ubuntu/artworks.jpg', BUCKET, file)
'''
below is the code to move the images file from "images directory" in EC2 to S3 >
'''
for file in imageFile:
        path = os.path.join(sourceDir, file)
        print(path)
        print(file)
        s3.meta.client.upload_file(path ,BUCKET,file)

