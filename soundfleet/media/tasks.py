import ffmpeg
import hashlib
import os
import shutil
import tempfile

from celery import shared_task
from pathlib import Path
from media.fields import AudioFile

from media.models import AudioTrack


@shared_task()
def create_audio_track_from_uploaded_file(
    source_file: str,
    bitrate: str = "128k",
    track_type: str = "music",
) -> None:

    with open(source_file, "rb") as f:
        file_hash = hashlib.sha1(f.read()).hexdigest()

    if AudioTrack.objects.filter(file_hash=file_hash).exists():
        return

    file_name = f"{file_hash}.ogg"
    dest_dir = Path(tempfile.gettempdir()) / file_hash

    if not os.path.isdir(dest_dir):
        os.mkdir(dest_dir)

    dest_file = dest_dir / file_name

    try:
        ffmpeg.input(source_file).output(
            dest_file, acodec="libvorbis", ac=1, ar="44100", ab=bitrate
        ).run()

        with open(dest_file, "rb") as f:
            AudioTrack.objects.create(
                file=AudioFile(f, name=file_name),
                track_type=track_type,
                file_hash=file_hash,
            )
    finally:
        if os.path.exists(source_file):
            os.unlink(source_file)
        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir)
