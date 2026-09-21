import base64
import json
import threading

import numpy as np
import requests
import sounddevice as sd

TTS_STREAM_URL = "https://api.60db.ai/tts-stream"

# 60db default voice (see https://docs.60db.ai)
DEFAULT_VOICE_ID = "fbb75ed2-975a-40c7-9e06-38e30524a9a1"

# LINEAR16 is supported at 8/16/24/48 kHz; 24 kHz mono is a good default
DEFAULT_SAMPLE_RATE = 24000

# REST streaming limit: 5000 characters per request
MAX_TEXT_LENGTH = 5000


class SixtyDBError(RuntimeError):
    """Raised when the 60db TTS API returns an error."""


class SixtyDBTTS:
    """60db.ai text-to-speech speaker.

    Uses the 60db streaming endpoint (POST /tts-stream), which returns
    newline-delimited JSON chunks of base64-encoded LINEAR16 audio, and
    plays them through sounddevice as they arrive. Mirrors the behaviour
    of the RealtimeTTS ElevenLabs engine used in this project.
    """

    def __init__(self, api_key, voice_id=DEFAULT_VOICE_ID,
                 sample_rate=DEFAULT_SAMPLE_RATE, speed=1.0):
        self.api_key = api_key
        self.voice_id = voice_id
        self.sample_rate = sample_rate
        self.speed = speed

    def _payload(self, text):
        return {
            "text": text[:MAX_TEXT_LENGTH],
            "voice_id": self.voice_id,
            "audio_config": {
                "audio_encoding": "LINEAR16",
                "sample_rate_hertz": self.sample_rate,
            },
            "speed": self.speed,
        }

    def speak(self, text):
        """Synthesize and play `text` (blocks until playback finishes)."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        with sd.OutputStream(samplerate=self.sample_rate, channels=1,
                             dtype="int16") as player:
            with requests.post(TTS_STREAM_URL, json=self._payload(text),
                               headers=headers, stream=True,
                               timeout=(10, 120)) as response:
                if response.status_code != 200:
                    raise SixtyDBError(
                        f"60db TTS failed (HTTP {response.status_code}): "
                        f"{response.text[:300]}")
                for line in response.iter_lines(decode_unicode=True):
                    if not line:
                        continue
                    message = json.loads(line)
                    kind = message.get("type")
                    if kind == "chunk":
                        audio_b64 = (message.get("result") or {}).get("audioContent")
                        if not audio_b64:
                            continue
                        audio = base64.b64decode(audio_b64)
                        samples = np.frombuffer(audio, dtype=np.int16)
                        if samples.size:
                            player.write(samples.reshape(-1, 1))
                    elif kind == "error":
                        raise SixtyDBError(f"60db TTS error: {message}")
        return True

    def speak_async(self, text):
        """Same as speak() but runs in a background thread (like play_async)."""
        thread = threading.Thread(target=self._speak_worker, args=(text,),
                                  daemon=True)
        thread.start()
        return thread

    def _speak_worker(self, text):
        try:
            self.speak(text)
        except Exception as exc:
            print(f"[sixtydb] playback failed: {exc}")
