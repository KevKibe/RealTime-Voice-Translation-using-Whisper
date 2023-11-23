from flask import Flask, request, jsonify
from text_translate import TextTranslator

app = Flask(__name__)

translator = TextTranslator()

@app.route('/translate', methods=['POST'])
def translate():
    """
    Endpoint for translating text to the specified target language.

    Expects a JSON payload with 'text' and 'target_language' keys.

    :return: JSON response with the translated text.
    """
    data = request.get_json()

    if not all(key in data for key in ['text', 'target_language']):
        return jsonify({'error': 'Missing required parameters'}), 400

    text_to_translate = data['text']
    target_language = data['target_language']

    translation_result = translator.translate_text(text_to_translate, target_language)
    translated_text = translation_result["translatedText"]

    return jsonify({'translated_text': translated_text})

if __name__ == '__main__':
    app.run(debug=True)
