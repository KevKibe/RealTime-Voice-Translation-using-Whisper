# Description
- This is a simple language translation application built using Streamlit.
  The application allows users to record speech, transcribe it using the Whisper ASR (Automatic Speech Recognition) model, translate the transcribed text into a selected language, and play back the translated text using the Elevenlabs TTS (Text-to-Speech) engine.

## Features
- **Speech Transcription:** Utilizes the Whisper ASR model to transcribe recorded speech.
- **Language Translation:** Translates the transcribed text into the selected language using a translation API.
- **Text-to-Speech:** Converts the translated text into audio using either the Elevenlabs TTS engine or the 60db.ai TTS engine (streaming).
- **Language Options:** Supports translation into multiple languages, including Afrikaans, Amharic, Arabic, Hausa, Igbo, Sesotho, Swahili, Xhosa, Yoruba, Zulu, and Shona.

## How to Use
- Select the target language from the dropdown list.
- Select the Text-to-Speech engine (ElevenLabs or 60db). The 60db option only appears when a 60db API key is configured. Note: 60db TTS speaks English and Indic languages (auto-detected from the text); for the African languages above, prefer ElevenLabs.
- Click the ```Tap to Speak``` button to record speech. The recording duration is limited to 10 seconds.
- After recording, the transcribed text and translated text will be displayed.
- The translated text will be played back using the Text-to-Speech engine, and the duration of the audio will be shown.

## Installation
Ensure you have the required dependencies installed by running:
```
pip install -r requirements.txt
```
Set up the necessary API keys in `.streamlit/secrets.toml`:
```
[elevenlabs]
keys = "your_elevenlabs_api_key_here"

[sixtydb]
api_key = "your_60db_api_key_here"
```
The `[sixtydb]` entry is optional; without it the app runs with ElevenLabs only. Alternatively, the 60db key can be provided via the `SIXTYDB_API_KEY` environment variable in a .env file.
## Running the App
Execute the following command to run the Streamlit app:
```
streamlit run app.py
```
