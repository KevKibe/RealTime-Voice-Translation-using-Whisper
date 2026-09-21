class MockResponse:
    def __init__(self, status_code, payload=None, text=""):
        self.status_code = status_code
        self._payload = payload or {}
        self.text = text

    def json(self):
        return self._payload


def test_translate_returns_json_on_success(monkeypatch):
    from text_translate import Translator

    captured = {}

    def fake_post(url, json):
        captured["url"] = url
        captured["json"] = json
        return MockResponse(200, {"translated_text": "hola"})

    monkeypatch.setattr("text_translate.requests.post", fake_post)

    translator = Translator("https://example.com/translate")
    result = translator.translate("hello", "es")

    assert result == {"translated_text": "hola"}
    assert captured["url"] == "https://example.com/translate"
    assert captured["json"] == {"text": "hello", "target_language": "es"}


def test_translate_returns_error_message_on_failure(monkeypatch):
    from text_translate import Translator

    def fake_post(url, json):
        return MockResponse(500, text="internal error")

    monkeypatch.setattr("text_translate.requests.post", fake_post)

    translator = Translator("https://example.com/translate")
    result = translator.translate("hello", "es")

    assert result == "Error: 500, internal error"
