import whisper
import numpy as np
import sounddevice as sd
from playsound import playsound
import scipy.io.wavfile as wav


class WhisperTranscriber:
    def __init__(self, model="tiny"):
        """
        Initializes an instance of the WhisperTranslator class.

        :param model: The path to the Whisper ASR model. Defaults to "tiny".
        """
        self.model = whisper.load_model(model)

    def play_ding_sound(self, sound_file):
        playsound(sound_file)

    def transcribe(self, duration=10, fs=44100):
        """
        Transcribes the audio file using the Whisper ASR model and translates the result to the specified language.

        :param audio_path: The path to the audio file for transcription.
        :param target_language: The target language code for translation. Defaults to 'en' (English).
        :return: The transcribed and translated text.
        """
        self.play_ding_sound("notification-sound-7062.wav")
        print("Recording...")
        myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        print("Recording complete!")
        self.play_ding_sound("notification-sound-7062.wav")

        wav.write('recording.wav', fs, myrecording)

        result = self.model.transcribe('recording.wav')
        transcribed_text = result['text']
        return transcribed_text

# whisper_translator = WhisperTranscriber()
# transcription = whisper_translator.transcribe()
# print(transcription)
