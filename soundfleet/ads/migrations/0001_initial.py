# Generated by Django 3.2 on 2022-02-23 10:01

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
            name="AdBlock",
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
                "verbose_name": "Ad block",
                "verbose_name_plural": "Ad blocks",
            },
        ),
        migrations.CreateModel(
            name="AdPlaylist",
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
                "verbose_name": "Ad playlist",
                "verbose_name_plural": "Ad playlists",
            },
        ),
        migrations.CreateModel(
            name="AdTrack",
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
                ("rank", models.PositiveSmallIntegerField(default=1)),
                (
                    "playlist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ads.adplaylist",
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
                "verbose_name": "Ad track",
                "verbose_name_plural": "Ad tracks",
            },
        ),
        migrations.CreateModel(
            name="AdSchedule",
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
                    "ad_blocks",
                    models.ManyToManyField(
                        through="ads.AdBlock", to="ads.AdPlaylist"
                    ),
                ),
            ],
            options={
                "verbose_name": "Ad schedule",
                "verbose_name_plural": "Ad schedules",
            },
        ),
        migrations.AddField(
            model_name="adplaylist",
            name="tracks",
            field=models.ManyToManyField(
                through="ads.AdTrack", to="media.AudioTrack"
            ),
        ),
        migrations.AddField(
            model_name="adblock",
            name="playlist",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="ads.adplaylist",
            ),
        ),
        migrations.AddField(
            model_name="adblock",
            name="schedule",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="ads.adschedule",
            ),
        ),
    ]
