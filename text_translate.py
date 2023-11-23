import os
from google.oauth2 import service_account
from google.cloud import translate_v2 as translate


class TextTranslator:
    def __init__(self, credentials_path='/Users/la/Desktop/Projects/Whisper/key.json'):
        """
        Initializes an instance of the TextTranslator class.

        :param credentials_path: The file path to the Google Cloud service account credentials JSON file.
                                 Defaults to '/Users/la/Desktop/Projects/Whisper/key.json'.
        """
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        self.translate_client = translate.Client()

    def translate_text(self, text, target_language='en'):
        """
        Translates the given text to the specified target language using the Google Cloud Translation API.

        :param text: The text to be translated.
        :param target_language: The target language code to which the text should be translated.
                               Defaults to 'en' (English).
        :return: The translated text.
        """
        result = self.translate_client.translate(text, target_language=target_language)
        return result



# translator = TextTranslator()
# target_language = 'hi'
# text_to_translate = "Hello, my name is Kevin"
# translation_result = translator.translate_text(text_to_translate, target_language)
# print(translation_result["translatedText"])


