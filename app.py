import streamlit as st
from whisp_transcription import WhisperTranscriber
from text_translate import Translator
import time
import os
from RealtimeTTS import ElevenlabsEngine, TextToAudioStream
from elevenlabs import generate, play, set_api_key, stream, clone
from dotenv import load_dotenv
from sixtydb_tts import SixtyDBTTS

elevenlabs_api_key = st.secrets["elevenlabs"]["keys"]
# elevenlabs_api_key = os.getenv('ELLEVEN_LABS_API')
set_api_key(elevenlabs_api_key)

@st.cache_resource
def get_sixtydb_tts(api_key):
    return SixtyDBTTS(api_key)

def main():
    st.title("Language Translation App")
    load_dotenv()

    try:
        sixtydb_api_key = st.secrets["sixtydb"]["api_key"]
    except (KeyError, FileNotFoundError):
        sixtydb_api_key = os.getenv("SIXTYDB_API_KEY")
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
    engine_options = ['ElevenLabs', '60db'] if sixtydb_api_key else ['ElevenLabs']
    selected_engine = st.selectbox('Text-to-Speech Engine:', engine_options)
    if selected_engine == '60db':
        st.caption('60db TTS speaks English and Indic languages (auto-detected from the text). For the African languages above, prefer ElevenLabs.')
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
        if selected_engine == '60db':
            get_sixtydb_tts(sixtydb_api_key).speak_async(translation)
        else:
            engine = ElevenlabsEngine()
            stream = TextToAudioStream(engine)
            stream.feed(translation)
            stream.play_async()
        end_time = time.time()
        duration = end_time - start_time
        st.write(f"Duration: {duration}")

if __name__ == "__main__":
    main()
