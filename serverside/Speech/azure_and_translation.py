import boto3
import requests
from requests.structures import CaseInsensitiveDict
import configparser,logging, sys
from os import path
from logging.handlers import RotatingFileHandler
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




def get_token(subscription_key, fetch_token_url):
    l.info("Retrieving access token")
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key
    }
    response = requests.post(fetch_token_url, headers=headers)
    access_token = str(response.text)
    return access_token
def get_audio_file(access_token, language, voice, expression, out_file, tts_string, api_url):
    # https://reqbin.com/req/python/c-xgafmluu/convert-curl-to-python-requests I love youuuu so much webmaster
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
        return True
    else:
        l.error("Error generating audio file: " + str(r.status_code) + " " + str(r.content))
        return False
# translating
def translator(text_to_translate, target):
    AWS_ACCESS_KEY_ID = config['amazon']['accessKey']
    AWS_SECRET_ACCESS_KEY = config['amazon']['secretKey']
    region = config['amazon']['region']
    translate = boto3.client(service_name='translate',
                             region_name=region,
                             aws_access_key_id=AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    #translate = boto3.client('translate', region_name='us-west-1', use_ssl=True)
    result = translate.translate_text(Text=text_to_translate,
                                      SourceLanguageCode="en",
                                      TargetLanguageCode=target
                                      )
    print(f'TranslatedText: {result["TranslatedText"]}')
    print('SourceLanguageCode: ' + result.get('SourceLanguageCode'))
    return result["TranslatedText"]
    print('TargetLanguageCode: ' + result.get('TargetLanguageCode'))
   #return text_to_translate, target_language_code

def main_function():


    subscription_key = config['azure']['subscription_key']
    region = config['azure']['region']
    fetch_token_url = config['azure']['fetch_token_url']
    api_url = config['azure']['text_to_speech_url']

    string_uuid = str(uuid.uuid1()) + ".mp3"
    file_name = string_uuid

    out_file = config['azure']['audio_file_output_location'] + file_name
    voice = "zh-CN-XiaoxiaoNeural"
    voice1= "vi-VN-HoaiMyNeural"
    language1="vi-VN"
    language = "zh-CN"
    tts_string = "冻结不要动 "
    #test translation
    text_to_translate= "good luck"
    result1= translator(text_to_translate, "vi")
    #tts_string = str(tts_string)
  #  result1 =str(result1)
  #  l.info(tts_string)
    l.info(result1)
    expression = "calm"
    access_token = get_token(subscription_key, fetch_token_url)
    get_audio_file(access_token, language1, voice1, expression, out_file, result1, api_url)
main_function()