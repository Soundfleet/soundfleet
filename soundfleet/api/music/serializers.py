from rest_framework.serializers import ModelSerializer, IntegerField

from music.models import MusicPlaylist


class MusicPlaylistSerializer(ModelSerializer):

    track_count = IntegerField(read_only=True)

    class Meta:
        model = MusicPlaylist
        exclude = []
