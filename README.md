# Description
- This is a simple language translation application built using Streamlit.
  The application allows users to record speech, transcribe it using the Whisper ASR (Automatic Speech Recognition) model, translate the transcribed text into a selected language, and play back the translated text using the Elevenlabs TTS (Text-to-Speech) engine.

## Features
- **Speech Transcription:** Utilizes the Whisper ASR model to transcribe recorded speech.
- **Language Translation:** Translates the transcribed text into the selected language using a translation API.
- **Text-to-Speech:** Converts the translated text into audio using the Elevenlabs TTS engine.
- **Language Options:** Supports translation into multiple languages, including Afrikaans, Amharic, Arabic, Hausa, Igbo, Sesotho, Swahili, Xhosa, Yoruba, Zulu, and Shona.

## How to Use
- Select the target language from the dropdown list.
- Click the ```Tap to Speak``` button to record speech. The recording duration is limited to 10 seconds.
- After recording, the transcribed text and translated text will be displayed.
- The translated text will be played back using the Text-to-Speech engine, and the duration of the audio will be shown.

## Installation
Ensure you have the required dependencies installed by running:
```
pip install -r requirements.txt
```
Set up the necessary API keys by creating a .env file and adding the Elevenlabs API key:
```
ELEVENLABS_API_KEY=your_api_key_here
```
## Running the App
Execute the following command to run the Streamlit app:
```
streamlit run app.py
```
