import requests

class Translator:
    def __init__(self, api_url):
        self.api_url = api_url

    def translate(self, text, target_language):
        data = {
            'text': text,
            'target_language': target_language
        }

        response = requests.post(self.api_url, json=data)

        if response.status_code == 200:
            return response.json()
        else:
            return f'Error: {response.status_code}, {response.text}'

# Usage
# translator = Translator('https://startupproject-391507.uc.r.appspot.com/translate')
# translation=translator.translate('Hello, world!', 'ar')
# print(translation['translated_text'])
