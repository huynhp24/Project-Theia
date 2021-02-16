import boto3
from PIL import Image
from io import BytesIO
import io

def printText(textDetections):
    sen = ''
    wordC = 0
    for text in textDetections:
        if (text['Type'] == 'WORD'):
            # print(text['DetectedText'])
            sen = sen + text['DetectedText'] + " "
            wordC += 1

        # print()
    print(sen)
    print("Text detected: " + str(wordC))

def imageBinary(photo,client):
    image = Image.open(photo)
    stream = io.BytesIO()
    image.save(stream, format=image.format)
    image_binary = stream.getvalue()
    response = client.detect_text(Image={'Bytes': image_binary})
    # print(response)
    textDetections = response['TextDetections']
    printText(textDetections)




def detect_text(photo, bucket):
    client = boto3.client('rekognition')
    try:
        response = client.detect_text(Image={'S3Object': {'Bucket': bucket, 'Name': photo}})

    except:
        # raise
        if (photo.endswith('png') or photo.endswith('jpg')):
            print("The photo is jpg and png format")
            imageBinary(photo, client)
        else:
            print("when calling the DetectText operation: Request has invalid image format ")
    else:
        textDetections = response['TextDetections']
        print('Detected text\n----------')
        printText(textDetections)
        # sen = ''
        # wordC = 0
        # for text in textDetections:
        #     print(text)
        #     print('Detected text:' + text['DetectedText'])
        #     print('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")
        #     print('Id: {}'.format(text['Id']))
        #     if 'ParentId' in text:
        #         print('Parent Id: {}'.format(text['ParentId']))
        #     print('Type:' + text['Type'])
        #     if(text['Type'] == 'WORD'):
        #
        #        # print(text['DetectedText'])
        #        sen = sen + text['DetectedText'] + " "
        #        wordC += 1
        #
        #     print()
        # print(sen)

        # print("Text detected: " + str(wordC))



def main():
    # photo = saveURL.img
    #
    # print(photo)
    bucket = 'bucket-image'
    photo = 'picWords.JPG'
    text_count = detect_text(photo, bucket)
    # print("Text detected: " + str(text_count))


if __name__ == "__main__":
    main()