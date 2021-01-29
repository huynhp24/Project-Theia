
import azure.cognitiveservices.speech as speechsdk

# Put your subscription key and region
speech_key=""
service_region = ""

#text to speech function, input is a string, output is audio from your speaker
def text_to_speech_function(text):
    speech_config = speechsdk.SpeechConfig(subscription=speech_key,region=service_region)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    # Synthesizing the result
    result = speech_synthesizer.speak_text_async(text).get()


#call text_to_speech_function for testing
text = "speak this string"
text_to_speech_function(text)