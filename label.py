import boto3
from pprint import pprint
import image_helper


client = boto3.client('rekognition')
#  local storage
# imgfilename = 'Images/chevysonic.jpg'
# imgbytes = image_helper.get_image_from_file(imgfilename)
#
# rekresp = client.detect_labels(Image={'Bytes': imgbytes},
#                                MinConfidence = 90
#                                )
#
# print("List all the items in the image:")
#
# for label in rekresp['Labels']:
#     pprint(label['Named'])


 # recognition from aws S3 bucket
photo = 'ams-repair-iss-640x353.jpg'
response = client.detect_labels(Image = {'S3Object': {
                                'Bucket' : 'seniorpj',
                                'Name' : photo
                }},
                MinConfidence = 95)

# for label in
print(response)
for label in response['Labels']:
    print(label['Name'])