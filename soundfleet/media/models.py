from django.conf import settings
from django.db import models

from .fields import AudioField


storage_module, storage_class = settings.AUDIO_TRACKS_STORAGE[
    "storage_class"
].rsplit(".", 1)

Storage = getattr(
    __import__(
        storage_module,
        globals(),
        locals(),
        [storage_class],
    ),
    storage_class,
)

audio_tracks_storage = Storage(**settings.AUDIO_TRACKS_STORAGE["storage_conf"])


class AudioTrack(models.Model):
    class TrackTypes(models.TextChoices):
        MUSIC = "music", "Music"
        AD = "ad", "Ad"

    track_type = models.CharField(max_length=5, default="music")
    artist = models.CharField("artist", max_length=512, blank=True, default="")
    title = models.CharField("title", max_length=512, blank=True, default="")
    genre = models.CharField("genre", max_length=512, blank=True, default="")
    size = models.PositiveIntegerField("size", default=0, editable=False)
    length = models.PositiveIntegerField("length", default=0, editable=False)

    file = AudioField(
        storage=audio_tracks_storage,
        artist_field="artist",
        title_field="title",
        genre_field="genre",
        length_field="length",
        size_field="size",
        max_length=255,
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    file_name = models.CharField(max_length=256)

    # store original file hash to avoid repetition
    file_hash = models.CharField(max_length=40)

    def __str__(self):
        return (
            f"{self.artist or 'Unknown artist'}"
            f" - {self.title or 'Unknown title'}"
        )
