
import azure.cognitiveservices.speech as speechsdk
import uuid

speech_key=""
service_region = ""



def text_to_speech_function(text):
    speech_config = speechsdk.SpeechConfig(subscription=speech_key,region=service_region)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    # Synthesizing the result
    result = speech_synthesizer.speak_text_async(text).get()



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
    return file_name



#text_to_speech_function("hello Ardee, Welcome to Las vegas")
text = input()
speech_synthesis_to_mp3_file(text)
