import boto3
def translator(text_to_translate, translating_language):
    translate = boto3.client('translate')
    result = translate.translate_text(Text = text_to_translate,
                                  SourceLanguageCode="en",
                                  TargetLanguageCode=translating_language)
    print(f'TranslatedText: {result["TranslatedText"]}')
    return result


text = "welcome"
translator(text, "fr")
