import boto3
import image_helper
from pprint import pprint
import sys
import json
'''
   This is textract rekognition for images
'''
# Amazon textract
# textract = boto3.client(
# service_name = 'textract',
# region_name = 'us-west-1')

# Amazon Textract client
textract = boto3.client('textract')
s3 = boto3.resource('s3')

imgfilename = 'Images/coffeeText.JPG'
imgbytes = image_helper.get_image_from_file(imgfilename)

response = textract.detect_document_text(
        Document ={ 'Bytes': imgbytes})
pprint(response)
text = ''
for item in response['Blocks']:
    if item["BlockType"] == "LINE":
        print('\033[94m' + item["Text"] + '\033[0m')
        # print(item['Text'])
        # text = text + " " +item["Text"]
#################################################



# -------------------------------------------------------------
# columns = []
# lines = []
# for item in response["Blocks"]:
#       if item["BlockType"] == "LINE":
#         column_found=False
#         for index, column in enumerate(columns):
#             bbox_left = item["Geometry"]["BoundingBox"]["Left"]
#             bbox_right = item["Geometry"]["BoundingBox"]["Left"] + item["Geometry"]["BoundingBox"]["Width"]
#             bbox_centre = item["Geometry"]["BoundingBox"]["Left"] + item["Geometry"]["BoundingBox"]["Width"]/2
#             column_centre = column['left'] + column['right']/2
#
#             if (bbox_centre > column['left'] and bbox_centre < column['right']) or (column_centre > bbox_left and column_centre < bbox_right):
#                 #Bbox appears inside the column
#                 lines.append([index, item["Text"]])
#                 column_found=True
#                 break
#         if not column_found:
#             columns.append({'left':item["Geometry"]["BoundingBox"]["Left"], 'right':item["Geometry"]["BoundingBox"]["Left"] + item["Geometry"]["BoundingBox"]["Width"]})
#             lines.append([len(columns)-1, item["Text"]])
#
# lines.sort(key=lambda x: x[0])
# for line in lines:
#     print (line[1])