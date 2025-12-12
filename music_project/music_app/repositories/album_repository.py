from .base_repository import BaseRepository
from music_app.models import Album
from django.db.models import Count

class AlbumRepository(BaseRepository):
    model = Album

    def get_top_albums(self, limit=10):
        return Album.objects.annotate(filtered_track_count=Count('song')).order_by('-filtered_track_count')[:limit]
