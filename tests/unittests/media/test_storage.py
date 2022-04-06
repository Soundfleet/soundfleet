import os
import pytest

from pathlib import Path

from soundfleet.media.models import audio_tracks_storage


test_resources = (
    Path(os.path.dirname(__file__)) / ".." / ".." / "test_resources"
)


@pytest.mark.parametrize(
    "path,expected",
    [
        (
            test_resources / "correct-1.mp3",
            "b83c0ba0ad392d8241b49386d6f093eafc710551.mp3",
        ),
        (
            test_resources / "correct-1.ogg",
            "1327ecb79f87a583aa586ec7b809173e55a0a54e.ogg",
        ),
        (
            test_resources / "invalid.xyz",
            "bb4377b3f57257ca7cd3076065f1cdf3cf1a7e91",
        ),
    ],
)
def test_get_hashed_name(path: str, expected: str):
    with open(path, "rb") as f:
        name = audio_tracks_storage.get_hashed_name(f)
        assert name == expected
