import pytest

from app.speech_output import SpeechSynthesisResult, synthesize_checked


class FakeSynthesizer:
    provider_name = "test"
    model_name = "test-tts"
    model_version = None
    voice_name = "test-voice"

    def __init__(self, result=None):
        self.result = result or SpeechSynthesisResult(audio=b"ID3fake", media_type="audio/mpeg")
        self.received = None

    def synthesize(self, *, text: str):
        self.received = text
        return self.result


def test_synthesis_normalizes_bounded_text():
    provider = FakeSynthesizer()
    result = synthesize_checked(provider, text="  Explain   the architecture.  ")
    assert provider.received == "Explain the architecture."
    assert result.media_type == "audio/mpeg"
    assert result.audio == b"ID3fake"


@pytest.mark.parametrize("text", ["", "   ", "x" * 1201])
def test_synthesis_rejects_invalid_text(text):
    with pytest.raises(ValueError):
        synthesize_checked(FakeSynthesizer(), text=text)


def test_synthesis_rejects_wrong_media_type():
    provider = FakeSynthesizer(SpeechSynthesisResult(audio=b"data", media_type="audio/wav"))
    with pytest.raises(ValueError):
        synthesize_checked(provider, text="Question")


def test_synthesis_rejects_oversized_audio():
    provider = FakeSynthesizer(SpeechSynthesisResult(audio=b"x" * (5 * 1024 * 1024 + 1), media_type="audio/mpeg"))
    with pytest.raises(ValueError):
        synthesize_checked(provider, text="Question")
