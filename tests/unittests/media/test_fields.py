import os
import pytest
import stat

from pathlib import Path

from soundfleet.media.fields import AudioFile
from soundfleet.media.models import AudioTrack


test_resources = (
    Path(os.path.dirname(__file__)) / ".." / ".." / "test_resources"
)


@pytest.mark.parametrize(
    "path,expected",
    [
        (
            test_resources / "correct-1.ogg",
            {
                "artist": "Scianka",
                "title": "(...)",
                "genre": "Alternative, Avant-Rock",
            },
        )
    ],
)
def test_metadata(path: str, expected: dict):
    with open(path, "rb") as f:
        file_size = os.stat(path)[stat.ST_SIZE]
        audio_file = AudioFile(f)
        for k, v in expected.items():
            assert getattr(audio_file, k) == v
        assert audio_file.size == file_size



@pytest.mark.parametrize(
    "path,expected",
    [
        (
            test_resources / "correct-1.ogg",
            {
                "artist": "Scianka",
                "title": "(...)",
                "genre": "Alternative, Avant-Rock",
                "length": 5
            },
        )
    ],
)
def test_audio_file_populates_metadata(path: str, expected: dict):
    with open(path, "rb") as f:
        file_size = os.stat(path)[stat.ST_SIZE]
        audio_file = AudioFile(f)
        audio_track = AudioTrack(file=audio_file)
        for k, v in expected.items():
            assert getattr(audio_track, k) == v
        assert audio_track.size == file_size