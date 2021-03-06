# Generated by Django 3.2 on 2022-02-22 12:40

from django.db import migrations, models
import django.db.models.deletion
import soundfleet.utils.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("media", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="MusicBlock",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start", models.TimeField()),
                ("end", models.TimeField()),
            ],
            options={
                "verbose_name": "Music block",
                "verbose_name_plural": "Music blocks",
            },
        ),
        migrations.CreateModel(
            name="MusicPlaylist",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=64, unique=True)),
                ("description", models.TextField(blank=True, default="")),
                (
                    "label_color",
                    soundfleet.utils.db.fields.ColorField(
                        default="#000000", max_length=7
                    ),
                ),
            ],
            options={
                "verbose_name": "Playlist",
                "verbose_name_plural": "Playlists",
            },
        ),
        migrations.CreateModel(
            name="MusicTrack",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "rank",
                    models.PositiveSmallIntegerField(default=1),
                ),
                (
                    "playlist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="music.musicplaylist",
                    ),
                ),
                (
                    "track",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="media.audiotrack",
                    ),
                ),
            ],
            options={
                "verbose_name": "Music track",
                "verbose_name_plural": "Music tracks",
            },
        ),
        migrations.CreateModel(
            name="MusicSchedule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=64, unique=True)),
                ("description", models.TextField(blank=True, default="")),
                (
                    "label_color",
                    soundfleet.utils.db.fields.ColorField(
                        default="#000000", max_length=7
                    ),
                ),
                (
                    "music_blocks",
                    models.ManyToManyField(
                        through="music.MusicBlock", to="music.MusicPlaylist"
                    ),
                ),
            ],
            options={
                "verbose_name": "Music schedule",
                "verbose_name_plural": "Music schedules",
            },
        ),
        migrations.AddField(
            model_name="musicplaylist",
            name="tracks",
            field=models.ManyToManyField(
                through="music.MusicTrack", to="media.AudioTrack"
            ),
        ),
        migrations.AddField(
            model_name="musicblock",
            name="playlist",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="music.musicplaylist",
            ),
        ),
        migrations.AddField(
            model_name="musicblock",
            name="schedule",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="music.musicschedule",
            ),
        ),
    ]
