from configparser import ConfigParser
import boto3


def detect_labels(photo, bucket):
    client = boto3.client('rekognition', 'us-west-1')

    response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
                                    MaxLabels=10)

    print('Detected labels for ' + photo)
    print()
    for label in response['Labels']:
        print("Label: " + label['Name'])
        print("Confidence: " + str(label['Confidence']))
        print("Instances:")
        for instance in label['Instances']:
            print("  Bounding box")
            print("    Top: " + str(instance['BoundingBox']['Top']))
            print("    Left: " + str(instance['BoundingBox']['Left']))
            print("    Width: " + str(instance['BoundingBox']['Width']))
            print("    Height: " + str(instance['BoundingBox']['Height']))
            print("  Confidence: " + str(instance['Confidence']))
            print()

        print("Parents:")
        for parent in label['Parents']:
            print("   " + parent['Name'])
        print("----------")
        print()
    return len(response['Labels'])

def detectText(documentName, s3BucketName):
    # Amazon Textract client
    textract = boto3.client('textract')

    # Call Amazon Textract
    response = textract.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': s3BucketName,
                'Name': documentName
            }
        })

    # Print detected text
    for item in response["Blocks"]:
        # print(item)
        if item["BlockType"] == "LINE":
            # print('\033[94m' + item["Text"] + '\033[0m')
            if item['Text'] == '800':
                print('Image has no text')
            else:
                print('\033[94m' + item["Text"] + '\033[0m')

def main():
    file = 'config.ini'
    config = ConfigParser()
    config.read(file)

    print(config.sections())
    print(list(config['account']))

    s3 = boto3.resource('s3')
    # print(s3.buckets.all())
    for bucket in s3.buckets.all():
        print(bucket)
    photo=config['account']['s3doc']
    print('doc: ', photo)
    bucket= config['account']['path']
    print('bucket name: ', bucket)
    label_count = detect_labels(photo, bucket)
    print("Labels detected for rekognition: " + str(label_count))

    detectText(photo, bucket)

if __name__ == "__main__":
    main()