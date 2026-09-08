import pytest

from app.speech import (
    MAX_AUDIO_BYTES,
    MAX_TRANSCRIPT_CHARS,
    TranscriptionResult,
    transcribe_checked,
    validate_audio_input,
    validate_transcription_result,
)


class FakeTranscriber:
    provider_name = "test"
    model_name = "speech-fixture"
    model_version = "1"

    def transcribe(self, *, audio: bytes, media_type: str):
        assert audio == b"audio"
        assert media_type == "audio/webm"
        return TranscriptionResult("  This is the transcript.  ", "en")


def test_audio_input_is_bounded_and_media_type_allowlisted():
    payload, media_type = validate_audio_input(b"audio", media_type="audio/webm; codecs=opus")
    assert payload == b"audio"
    assert media_type == "audio/webm"

    with pytest.raises(ValueError, match="empty"):
        validate_audio_input(b"", media_type="audio/webm")
    with pytest.raises(ValueError, match="maximum"):
        validate_audio_input(b"x" * (MAX_AUDIO_BYTES + 1), media_type="audio/webm")
    with pytest.raises(ValueError, match="unsupported"):
        validate_audio_input(b"audio", media_type="application/octet-stream")


def test_transcription_output_is_plain_bounded_text():
    result = validate_transcription_result(TranscriptionResult("  hello   world  ", "en"))
    assert result.text == "hello world"
    assert result.language == "en"

    with pytest.raises(ValueError, match="maximum"):
        validate_transcription_result(TranscriptionResult("x" * (MAX_TRANSCRIPT_CHARS + 1)))
    with pytest.raises(ValueError, match="empty"):
        validate_transcription_result(TranscriptionResult("   "))


def test_checked_transcription_validates_input_and_output():
    result = transcribe_checked(FakeTranscriber(), audio=b"audio", media_type="audio/webm")
    assert result.text == "This is the transcript."
    assert result.language == "en"
