from django.db import models

from utils.db.fields import ColorField


class MusicPlaylist(models.Model):

    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True, default="")
    label_color = ColorField(default="#000000")

    tracks = models.ManyToManyField(
        "media.AudioTrack", through="music.MusicTrack"
    )

    class Meta:
        verbose_name = "Playlist"
        verbose_name_plural = "Playlists"

    def __str__(self) -> str:
        return f"{self.name}"


class MusicTrack(models.Model):

    playlist = models.ForeignKey(MusicPlaylist, on_delete=models.CASCADE)
    track = models.ForeignKey("media.AudioTrack", on_delete=models.CASCADE)
    rank = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = "Music track"
        verbose_name_plural = "Music tracks"

    def __str__(self) -> str:
        return f"{str(self.playlist)}, {str(self.track)}"


class MusicSchedule(models.Model):

    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True, default="")
    label_color = ColorField(default="#000000")

    music_blocks = models.ManyToManyField(
        MusicPlaylist, through="music.MusicBlock"
    )

    class Meta:
        verbose_name = "Music schedule"
        verbose_name_plural = "Music schedules"

    def __str__(self) -> str:
        return f"{self.name}"


class MusicBlock(models.Model):

    playlist = models.ForeignKey(MusicPlaylist, on_delete=models.CASCADE)
    schedule = models.ForeignKey(MusicSchedule, on_delete=models.CASCADE)
    start = models.TimeField()
    end = models.TimeField()

    class Meta:
        verbose_name = "Music block"
        verbose_name_plural = "Music blocks"

    def __str__(self) -> str:
        return (
            f"{str(self.playlist)} of {str(self.schedule)} "
            f"from {self.start} to {self.end}"
        )
