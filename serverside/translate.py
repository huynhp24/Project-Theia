import boto3
import requests
from requests.structures import CaseInsensitiveDict
import configparser,logging, sys, os
from os import path
from logging.handlers import RotatingFileHandler
# from google_trans_new import google_translator
import uuid
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
logfile = config['logging']['logdir'] + "/azuretts.log"
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

#set up amazon
S3PATH = config['amazon']['bucket']
REGION = config['amazon']['region']
s3 = boto3.client('s3', region_name=REGION)
aws_translate = boto3.client('translate', region_name=REGION)


def get_token(subscription_key, fetch_token_url):
    l.info("Retrieving access token")
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key
    }
    response = requests.post(fetch_token_url, headers=headers)
    access_token = str(response.text)
    return access_token

def get_audio_file(access_token, language, voice, expression, out_file, tts_string, api_url):
    l.info("Generating audio file")
    headers = CaseInsensitiveDict()
    headers["Authorization"] = "Bearer " + access_token
    headers["Content-Type"] = "application/ssml+xml"
    headers["X-Microsoft-OutputFormat"] = "audio-48khz-192kbitrate-mono-mp3"
    data = """
<speak version="1.0" encoding="UTF-8" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang=\"""" + language + """\">
    <voice name=\"""" + voice + """\">
        <mstts:express-as style=\"""" + expression + """\">
            \'""" + tts_string + """\'
        </mstts:express-as>
    </voice>
</speak>
    """
    r = requests.post(api_url, headers=headers, data=data.encode('utf-8'))
    if r.status_code == 200:
        l.info("Successfully generated audio file")
        l.info("Saving file to " + out_file)
        with open(out_file, 'wb') as f:
            f.write(r.content)

        with open(out_file, 'rb') as f:
            s3.upload_fileobj(f, S3PATH, os.path.basename(out_file))
        url = "https://%s.s3-%s.amazonaws.com/%s" % (S3PATH, REGION, os.path.basename(out_file))
        l.info('printing URL : ' + url)
        os.remove(out_file)
        return url
    else:
        l.error("Error generating audio file: " + str(r.status_code) + " " + str(r.content))
        return False

# using google translate service
def translator(text_to_translate, target):
    # tr = google_translator()
    # lan = tr.translate(text_to_translate, lang_tgt=target)

    lan = aws_translate.translate_text(SourceLanguageCode="en", TargetLanguageCode=target, Text=text_to_translate)

    return lan

def textToSpeech( tts_string, uuid ,voice):
    subscription_key = config['azure']['subscription_key']
    region = config['azure']['region']
    fetch_token_url = config['azure']['fetch_token_url']
    api_url = config['azure']['text_to_speech_url']
    out_file = config['azure']['audio_file_output_location'] + uuid + '.mp3'
    language = voice[:5]
    target_lan = language[:2]

    print('language: ' + language)
    print('target language to translate: ' + target_lan)
    # getting the translated text back from google translate
    translation = translator(tts_string, target_lan)
    translation_string = translation["TranslatedText"]

    l.info("Getting translating result "+ translation_string)
    expression = "calm"
    access_token = get_token(subscription_key, fetch_token_url)
    url = get_audio_file(access_token, language, voice, expression, out_file, translation_string, api_url)
    return url, translation_string
