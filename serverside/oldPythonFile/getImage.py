import os
import boto3
from configparser import ConfigParser
from pprint import pprint


config = ConfigParser()
#print(os.getcwd())
sourceDir = config.get('/home/ubuntu/images')
#file = 'artworks.jpg'
s3 = boto3.resource('s3')
BUCKET = "bucket-image"


#print(os.listdir( sourceDir ))
imageFile = os.listdir(sourceDir)


#s3.meta.client.upload_file('/home/ubuntu/artworks.jpg', BUCKET, file)
'''
below is the code to move the images file from "images directory" in EC2 to S3 bucket
'''
for file in imageFile:
        path = os.path.join(sourceDir, file)
        print(path)
        print(file)
#       print(os.stat(path))

        s3.meta.client.upload_file(path ,BUCKET,file)
        print('Sucessfully move ' + file + " to S3 bucket: " + BUCKET)
        '''
        Removing images file from imges directory on EC2 once the file has been load to S3 bucket
        '''
        os.remove(path)
        print("Removing " + file + " from " + path)


#print(os.stat(imageFile))
'''
for delfile in imageFile:
        if delfile.endswith('.png') or delfile.endswith('.jpg'):
                os.remove(delfile)
                print("Removing " + file + "in " +path)
'''


