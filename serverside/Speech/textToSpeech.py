import azure.cognitiveservices.speech as speechsdk
import uuid
import logging
import boto3
from botocore.exceptions import ClientError


speech_key=""
service_region = ""
bucket = ""


def speech_synthesis_to_mp3_file(text):
    #configuring speechsdk
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    #output format is set to be mp3
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3  )
    #creating uuid for the mp3 file for a unique name
    string_uuid = str(uuid.uuid1()) + ".mp3"
    file_name = string_uuid
    file_config = speechsdk.audio.AudioOutputConfig(filename=file_name)
    #speech synthesizer
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)
    result = speech_synthesizer.speak_text_async(text).get()
    return result, file_name


def upload_file(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# translating
def translator(text_to_translate):
    translate = boto3.client('translate', region_name='us-west-1', use_ssl=True)
    result = translate.translate_text(Text=text_to_translate,
                                      SourceLanguageCode="en",
                                      TargetLanguageCode="de"
                                      )
    print(f'TranslatedText: {result["TranslatedText"]}')
    print('SourceLanguageCode: ' + result.get('SourceLanguageCode'))
    print('TargetLanguageCode: ' + result.get('TargetLanguageCode'))
   #return text_to_translate, target_language_code

#text to speech function, input is a string, output is audio from your speaker
def text_to_speech_function(text):
    speech_config = speechsdk.SpeechConfig(subscription=speech_key,region=service_region)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    # Synthesizing the result
    result = speech_synthesizer.speak_text_async(text).get()

def Speak_in_different_lang(text, target_lang):
       speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
       speech_config.speech_synthesis_language = target_lang
       speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
       result = speech_synthesizer.speak_text_async(text).get()


#text3="buona giornata"
#Speak_in_different_lang(text3, "it-IT")


#testing function
def test_text_to_speech_and_s3():
    print("type something here")
    text = input()
    text_to_speech_function(text)
    result, file_name = speech_synthesis_to_mp3_file(text)
    upload_file(file_name, bucket)
    print('done, uploaded the text to speech mp3 file to s3 bucket')
test_text_to_speech_and_s3()
translator("hello")