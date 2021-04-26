import sys
from os import path
import azure.cognitiveservices.speech as speechsdk
import uuid
import logging
import boto3
from botocore.exceptions import ClientError
import logging
from logging.handlers import RotatingFileHandler
import configparser
import requests
from requests.structures import CaseInsensitiveDict
import configparser,logging, sys
from os import path
from logging.handlers import RotatingFileHandler
# Reading config file
config = configparser.ConfigParser()
config.sections()
try:
    if path.exists(sys.argv[1]):
        config.read(sys.argv[1])
except IndexError:
    if path.exists('/opt/theia/config.ini'):
        config.read('/opt/theia/config.ini')
    elif path.exists('config.ini'):
        config.read('config.ini')
    else:
        print("No config file found")
# Setup logging
logfile = config['logging']['logdir'] + "azuretts.log" #
log_lvl = config['logging']['loglevel']
log_out = config['logging']['log_stream_to_console']
my_handler = RotatingFileHandler(logfile)
my_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(funcName)s (%(lineno)d) %(message)s'))
l = logging.getLogger(__name__)
l.setLevel(log_lvl.upper())
l.addHandler(my_handler)
if log_out.upper() == 'TRUE':
    l.addHandler(logging.StreamHandler())
l.info("Running Azure TTS")



speech_key = config['azure']['subscription_key']
service_region = config['azure']['region']
bucket = config['amazon']['s3Bucket']

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

def neural_voice_in_different_language1(text ,target_lang, target_voice):
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3  )
    string_uuid = str(uuid.uuid1()) + ".mp3"
    file_name = string_uuid
    file_config = speechsdk.audio.AudioOutputConfig(filename=file_name)

    speech_config.speech_synthesis_language = target_lang
    speech_config.speech_synthesis_voice_name =target_voice
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
def translator(text_to_translate, target):
    translate = boto3.client('translate', region_name='us-west-1', use_ssl=True)
    result = translate.translate_text(Text=text_to_translate,
                                      SourceLanguageCode="en",
                                      TargetLanguageCode=target
                                      )
    print(f'TranslatedText: {result["TranslatedText"]}')
    print('SourceLanguageCode: ' + result.get('SourceLanguageCode'))
    print('TargetLanguageCode: ' + result.get('TargetLanguageCode'))
    return result["TranslatedText"]
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



def neural_voice_in_different_language(text ,target_lang, target_voice):
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_synthesis_language = target_lang
    speech_config.speech_synthesis_voice_name =target_voice
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    result = speech_synthesizer.speak_text_async(text).get()


#text_to_speech_function("hello Ardee, Welcome to Las vegas")


neural_voice_in_different_language("có một buổi sáng tốt", "vi-VN","vi-VN-HoaiMyNeural")

#testing function
def test_text_to_speech_and_s3():
    print("type something here")
    text = input()
    text_to_speech_function(text)
    result, file_name = speech_synthesis_to_mp3_file(text)
    upload_file(file_name, bucket)
    print('done, uploaded the text to speech mp3 file to s3 bucket')
#test_text_to_speech_and_s3()
#result_translation= translator("hello", "vi")

def test_function():
    text1 = " have a good night"
    translate_to = "vi"
    speech_language = "vi-VN"
    speech_neural_language = "vi-VN-HoaiMyNeural"
    result_translation = translator(text1, translate_to)
    print(result_translation)
    print(type(result_translation))
#text3="buona giornata"
#Speak_in_different_lang(text3, "it-IT")

#result1, file_name1= neural_voice_in_different_language1(result_translation, speech_language, speech_neural_language)

#upload_file(file_name1, bucket)


