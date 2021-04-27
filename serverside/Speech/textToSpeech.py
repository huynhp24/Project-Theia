
import azure.cognitiveservices.speech as speechsdk
import uuid
import logging
import boto3
from azure.cognitiveservices.speech import AudioDataStream, SpeechSynthesizer, SpeechConfig
from botocore.exceptions import ClientError

speech_key = ""
service_region =
bucket = ""
# speak out loud
def text_to_speech_function(text):
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    # Synthesizing the result
    result = speech_synthesizer.speak_text_async(text).get()

def speech_synthesis_to_mp3_file(text):
    # configuring speechsdk
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # output format is set to be mp3
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
    # creating uuid for the mp3 file for a unique name
    string_uuid = str(uuid.uuid1()) + ".mp3"
    file_name = string_uuid
    file_config = speechsdk.audio.AudioOutputConfig(filename=file_name)
    # speech synthesizer
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)
    result = speech_synthesizer.speak_text_async(text).get()
    return result, file_name

# upload mp3 to s3
def upload_file(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')

    response = s3_client.upload_file(file_name, bucket, object_name)


# testing function
def test_text_to_speech_and_s3():
    print("type something here")
    text = input()
    text_to_speech_function(text)
    result, file_name = speech_synthesis_to_mp3_file(text)
    upload_file(file_name, bucket)
    print('done, uploaded the text to speech mp3 file to s3 bucket')



# translating
def translator(text_to_translate, target_language_code):
    translate = boto3.client('translate', region_name='us-west-1', use_ssl=True)
    result = translate.translate_text(Text=text_to_translate,
                                      SourceLanguageCode="en",
                                      TargetLanguageCode=target_language_code
                                      )
    print(f'TranslatedText: {result["TranslatedText"]}')
    return text_to_translate, target_language_code


# see target_lang input in https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support


def neural_voice_in_different_language(text ,target_lang, target_voice):
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_synthesis_language = target_lang
    speech_config.speech_synthesis_voice_name =target_voice
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    result = speech_synthesizer.speak_text_async(text).get()


neural_voice_in_different_language("có một buổi sáng tốt", "vi-VN","vi-VN-HoaiMyNeural")
