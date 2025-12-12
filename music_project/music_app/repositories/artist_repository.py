from .base_repository import BaseRepository
from music_app.models import Artist, Song
from django.db.models import Sum, Avg, Count

class ArtistRepository(BaseRepository):
    def __init__(self):
        super().__init__(Artist)

    def get_songs(self, artist_id):
        artist = self.get_by_id(artist_id)
        if not artist:
            return []
        return Song.objects.filter(main_artist=artist)

    def get_listeners_report(self):
            report = self.model.objects.aggregate(
                total_listeners=Sum('listeners'),
                average_listeners=Avg('listeners'),
                total_artists=Count('artist_id')
        )
            return report