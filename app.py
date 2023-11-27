import streamlit as st
from whisp_transcription import WhisperTranscriber
from text_translate import Translator
import time
import os
from RealtimeTTS import ElevenlabsEngine, TextToAudioStream
from elevenlabs import generate, play, set_api_key, stream, clone
from dotenv import load_dotenv

elevenlabs_api_key = st.secrets["elevenlabs"]["keys"]
# elevenlabs_api_key = os.getenv('ELLEVEN_LABS_API')
set_api_key(elevenlabs_api_key)

def main():
    st.title("Language Translation App")
    load_dotenv()
    languages = {
        'Afrikaans': 'af',
        'Amharic': 'am',
        'Arabic': 'ar',
        'Hausa': 'ha',
        'Igbo': 'ig',
        'Sesotho': 'st',
        'Swahili': 'sw',
        'Xhosa': 'xh',
        'Yoruba': 'yo',
        'Zulu': 'zu',
        'Shona': 'sn'
    }
    selected_language = st.selectbox('Translate Speech  to:', list(languages.keys()))
    st.write("Tap the button below to record the speech to translate, after the ding. Recording time is limited to 10 sec.")
    if st.button('Tap to Speak'):
        whisper_translator = WhisperTranscriber()
        transcription = whisper_translator.transcribe()
        st.write(f"{transcription}")
        translator = Translator('https://startupproject-391507.uc.r.appspot.com/translate')
        language_code = languages[selected_language]
        translation = translator.translate(transcription, language_code)
        translation = translation['translated_text']
        st.write(f"{translation}")
        start_time = time.time()
        engine = ElevenlabsEngine()
        stream = TextToAudioStream(engine)
        stream.feed(translation)
        stream.play_async()
        end_time = time.time()
        duration = end_time - start_time
        st.write(f"Duration: {duration}")

if __name__ == "__main__":
    main()
