import boto3

def detect_labels(photo, bucket):

    client=boto3.client('rekognition', 'us-west-1')

    response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},
        MaxLabels=10)

    pretty_print(response, bucket, photo)

    return response['Labels']

def pretty_print(response, bucket, photo):
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
        label_count=len(response['Labels'])
        print("Labels detected: " + str(label_count))
        
# def main():
s3 = boto3.resource('s3')
#print(s3.buckets.all())
#for bucket in s3.buckets.all():
#    print(bucket)
