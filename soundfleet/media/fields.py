import os
import mutagen.oggvorbis
import tempfile

from django import forms
from django.core.files import File
from django.db import models
from django.db.models.fields.files import (
    FileDescriptor,
    FieldFile,
    FileField,
)


class AudioFile(File):
    def __get_artist(self):
        artist = self.metadata.get("artist") or ""
        return artist

    artist = property(__get_artist)

    def __get_title(self):
        title = self.metadata.get("title") or ""
        return title

    title = property(__get_title)

    def __get_genre(self):
        genre = self.metadata.get("genre") or ""
        return genre

    genre = property(__get_genre)

    def __get_length(self):
        length = self.metadata.get("total_time") or 0
        return length

    length = property(__get_length)

    def __get_metadata(self):
        if not hasattr(self, "_metadata_cache"):
            self.__cache_file_metadata()
        return self._metadata_cache

    metadata = property(__get_metadata)

    def __extract_tag_attrs(self, mf):
        attrs = {}
        if mf.tags is not None:
            for attr_name in "artist", "title", "album", "genre":
                attr_val = ",".join(mf.tags.get(attr_name, []))
                attrs.update(**{attr_name: attr_val})
        return attrs

    def __extract_info_attrs(self, mf):
        attrs = {}
        if mf.info is not None:
            attrs.update(bitrate=mf.info.bitrate / 1000)
            attrs.update(samplerate=mf.info.sample_rate)
            attrs.update(total_time=int(mf.info.length))
        return attrs

    def __cache_file_metadata(self):
        def __metadata(mf):
            metadata = {}
            metadata.update(**self.__extract_tag_attrs(mf))
            metadata.update(**self.__extract_info_attrs(mf))
            return metadata

        close = self.closed
        self.open()
        fd, tmp_file = tempfile.mkstemp()
        try:
            self.seek(0)
            os.write(fd, self.read())
            os.close(fd)
            self._metadata_cache = __metadata(
                mutagen.oggvorbis.OggVorbis(tmp_file)
            )
        except mutagen.oggvorbis.OggVorbisHeaderError:
            self._metadata_cache = {}
        finally:
            os.remove(tmp_file)
            if close:
                self.close()

    def __repr__(self):
        return self.name

    def __str__(self):
        return repr(self)


class AudioFileDescriptor(FileDescriptor):
    def __set__(self, instance, value):
        previous_file = instance.__dict__.get(self.field.name)
        super().__set__(instance, value)
        if previous_file is not None:
            self.field._update_metadata_fields(instance, force=True)


class AudioFieldFile(AudioFile, FieldFile):
    def delete(self, save=True):
        if hasattr(self, "_metadata_cache"):
            del self._metadata_cache
        super().delete(save)


class AudioField(FileField):

    attr_class = AudioFieldFile
    descriptor_class = AudioFileDescriptor
    description = "File path"

    def __init__(
        self,
        verbose_name=None,
        name=None,
        upload_to="",
        storage=None,
        artist_field=None,
        title_field=None,
        genre_field=None,
        length_field=None,
        size_field=None,
        **kwargs,
    ):
        self.artist_field = artist_field
        self.title_field = title_field
        self.genre_field = genre_field
        self.length_field = length_field
        self.size_field = size_field
        super().__init__(verbose_name, name, upload_to, storage, **kwargs)

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        models.signals.post_init.connect(
            self._update_metadata_fields, sender=cls
        )

    def _update_metadata_fields(self, instance, force=False, *args, **kwargs):
        """
        Updates metadata based on <metadata_property>_field
        :return: None
        """

        has_metadata_fields = any(
            [
                self.artist_field,
                self.title_field,
                self.length_field,
                self.genre_field,
            ]
        )
        if not has_metadata_fields:
            return

        # getattr will call the MusicFileDescriptor's __get__ method, which
        # coerces the assigned value into an instance of self.attr_class
        # (MusicFieldFile in this case).
        file = getattr(instance, self.attname)

        # Nothing to update if we have no file and not being forced to update.
        if not file and not force:
            return

        # Assume that there is something to update
        # when some fields are not filed
        # (ImageField has stronger assumption implemented)
        metadata_fields_filled = (
            not self.length_field or getattr(instance, self.length_field)
        ) or (not self.size_field or getattr(instance, self.size_field))
        if metadata_fields_filled and not force:
            return

        if file:
            artist = file.artist
            title = file.title
            genre = file.genre
            length = file.length
            size = file.size
        else:
            # No file, so clear metadata fields.
            artist = None
            title = None
            genre = None
            length = None
            size = None

        if self.artist_field and not getattr(instance, self.artist_field):
            setattr(instance, self.artist_field, artist)
        if self.title_field and not getattr(instance, self.title_field):
            setattr(instance, self.title_field, title)
        if self.genre_field and not getattr(instance, self.genre_field):
            setattr(instance, self.genre_field, genre)
        if self.length_field and not getattr(instance, self.length_field):
            setattr(instance, self.length_field, length)
        if self.size_field and not getattr(instance, self.size_field):
            setattr(instance, self.size_field, size)

    def formfield(self, **kwargs):
        defaults = {"form_class": forms.FileField}
        defaults.update(kwargs)
        return super().formfield(**defaults)
