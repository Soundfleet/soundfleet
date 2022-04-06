from django.db import models

from soundfleet.utils.db.fields import ColorField


class AdPlaylist(models.Model):

    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True, default="")
    label_color = ColorField(default="#000000")

    tracks = models.ManyToManyField("media.AudioTrack", through="ads.AdTrack")

    class Meta:
        verbose_name = "Ad playlist"
        verbose_name_plural = "Ad playlists"

    def __str__(self) -> str:
        return f"{self.name}"


class AdTrack(models.Model):

    playlist = models.ForeignKey(AdPlaylist, on_delete=models.CASCADE)
    track = models.ForeignKey("media.AudioTrack", on_delete=models.CASCADE)
    rank = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = "Ad track"
        verbose_name_plural = "Ad tracks"

    def __str__(self) -> str:
        return f"{str(self.playlist)}, {str(self.track)}"


class AdSchedule(models.Model):

    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True, default="")
    label_color = ColorField(default="#000000")

    ad_blocks = models.ManyToManyField(AdPlaylist, through="ads.AdBlock")

    class Meta:
        verbose_name = "Ad schedule"
        verbose_name_plural = "Ad schedules"

    def __str__(self) -> str:
        return f"{self.name}"


class AdBlock(models.Model):

    playlist = models.ForeignKey(AdPlaylist, on_delete=models.CASCADE)
    schedule = models.ForeignKey(AdSchedule, on_delete=models.CASCADE)
    start = models.TimeField()
    end = models.TimeField()

    class Meta:
        verbose_name = "Ad block"
        verbose_name_plural = "Ad blocks"

    def __str__(self) -> str:
        return (
            f"{str(self.playlist)} of {str(self.schedule)} "
            f"from {self.start} to {self.end}"
        )
