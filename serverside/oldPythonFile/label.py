import boto3
from pprint import pprint
def detect_labels(photo, bucket):

    client=boto3.client('rekognition', 'us-west-1')

    response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},
        MaxLabels=10)

    print('Detected labels for ' + photo)
    print()
    for label in response['Labels']:
        print ("Label: " + label['Name'])
        print ("Confidence: " + str(label['Confidence']))
        print ("Instances:")
        for instance in label['Instances']:
            print ("  Bounding box")
            print ("    Top: " + str(instance['BoundingBox']['Top']))
            print ("    Left: " + str(instance['BoundingBox']['Left']))
            print ("    Width: " +  str(instance['BoundingBox']['Width']))
            print ("    Height: " +  str(instance['BoundingBox']['Height']))
            print ("  Confidence: " + str(instance['Confidence']))
            print()

        print ("Parents:")
        for parent in label['Parents']:
            print ("   " + parent['Name'])
        print ("----------")
        print ()
    return len(response['Labels'])


def textractOrder(photo, bucket):
    s3 = boto3.resource('s3')
    client = boto3.client('textract')
    response = client.start_document_text_detection(
        DocumentLocation ={'S3Object': {'Bucket': bucket, 'Name': photo}})

    print('Detected texts in ' + photo)
    pprint(response)
    text = ''
    for item in response['Blocks']:
        if item["BlockType"] == "LINE":
            # print('\033[94m' + item["Text"] + '\033[0m')
            print(item['Text'])
            text = text + " " + item["Text"]
# def main():
s3 = boto3.resource('s3')
# print(s3.buckets.all())
for bucket in s3.buckets.all():
    print(bucket)
photo='coffeeText.JPG'
bucket='bucket-image'
label_count=detect_labels(photo, bucket)
print("Labels detected: " + str(label_count))

print('Textract\n')
textractOrder(photo, bucket)
print()