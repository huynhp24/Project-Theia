import azure.cognitiveservices.speech as speechsdk

# Put your subscription key and region
speech_key=""
service_region = ""
def text_to_speech_function(text):
    speech_config = Speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    text = "speeck this string"
    text_to_speech_function(text)