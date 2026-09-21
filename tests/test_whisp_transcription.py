import importlib
import sys
import types


def test_module_imports_without_heavy_runtime_dependencies():
    sys.modules.pop("whisp_transcription", None)
    module = importlib.import_module("whisp_transcription")
    assert hasattr(module, "WhisperTranscriber")


def _load_module_with_stubs(monkeypatch):
    state = {
        "loaded_model": None,
        "record_args": None,
        "wait_called": False,
        "wav_write_args": None,
        "transcribe_path": None,
        "ding_files": [],
    }

    class DummyModel:
        def transcribe(self, path):
            state["transcribe_path"] = path
            return {"text": "stub transcript"}

    def load_model(name):
        state["loaded_model"] = name
        return DummyModel()

    whisper_module = types.ModuleType("whisper")
    whisper_module.load_model = load_model

    sd_module = types.ModuleType("sounddevice")

    def rec(samples, samplerate, channels):
        state["record_args"] = {
            "samples": samples,
            "samplerate": samplerate,
            "channels": channels,
        }
        return "audio-buffer"

    def wait():
        state["wait_called"] = True

    sd_module.rec = rec
    sd_module.wait = wait

    playsound_module = types.ModuleType("playsound")

    def playsound(path):
        state["ding_files"].append(path)

    playsound_module.playsound = playsound

    wavfile_module = types.ModuleType("scipy.io.wavfile")

    def write(path, sample_rate, recording):
        state["wav_write_args"] = {
            "path": path,
            "sample_rate": sample_rate,
            "recording": recording,
        }

    wavfile_module.write = write

    scipy_module = types.ModuleType("scipy")
    scipy_io_module = types.ModuleType("scipy.io")
    numpy_module = types.ModuleType("numpy")

    monkeypatch.setitem(sys.modules, "whisper", whisper_module)
    monkeypatch.setitem(sys.modules, "sounddevice", sd_module)
    monkeypatch.setitem(sys.modules, "playsound", playsound_module)
    monkeypatch.setitem(sys.modules, "scipy", scipy_module)
    monkeypatch.setitem(sys.modules, "scipy.io", scipy_io_module)
    monkeypatch.setitem(sys.modules, "scipy.io.wavfile", wavfile_module)
    monkeypatch.setitem(sys.modules, "numpy", numpy_module)

    sys.modules.pop("whisp_transcription", None)
    module = importlib.import_module("whisp_transcription")

    return module, state


def test_whisper_transcriber_initializes_model(monkeypatch):
    module, state = _load_module_with_stubs(monkeypatch)

    module.WhisperTranscriber(model="base")

    assert state["loaded_model"] == "base"


def test_transcribe_records_and_returns_text(monkeypatch):
    module, state = _load_module_with_stubs(monkeypatch)
    transcriber = module.WhisperTranscriber(model="tiny")

    result = transcriber.transcribe(duration=2, fs=16000)

    assert result == "stub transcript"
    assert state["record_args"] == {"samples": 32000, "samplerate": 16000, "channels": 1}
    assert state["wait_called"] is True
    assert state["wav_write_args"] == {
        "path": "recording.wav",
        "sample_rate": 16000,
        "recording": "audio-buffer",
    }
    assert state["transcribe_path"] == "recording.wav"
    assert state["ding_files"] == ["notification-sound-7062.wav", "notification-sound-7062.wav"]
