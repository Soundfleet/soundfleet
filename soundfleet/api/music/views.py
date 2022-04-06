from django.db.models import Count
from soundfleet.music.models import MusicPlaylist
from soundfleet.api.views import BaseModelViewSet

from .serializers import MusicPlaylistSerializer


class MusicPlaylistViewSet(BaseModelViewSet):

    queryset = MusicPlaylist.objects.annotate(track_count=Count("tracks"))
    serializer_class = MusicPlaylistSerializer
