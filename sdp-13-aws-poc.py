import boto3
bucket = "project-theia-test"
key = "chevysonic.jpg"
accessKey='AKIAVIFHHUHTHFH4XWVR'
secretKey='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'
def detect_labels(bucket, key, max_labels=20, min_confidence=70, region="us-west-1"):
	rekognition = boto3.client("rekognition",aws_access_key_id = accessKey,aws_secret_access_key =secretKey, region_name=region)
	response = rekognition.detect_labels(
		Image={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
		MaxLabels=max_labels,
		MinConfidence=min_confidence,
	)
	return response['Labels']
for label in detect_labels(bucket, key):
	print("{Name} - {Confidence}%".format(**label))