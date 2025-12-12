from .base_repository import BaseRepository
from music_app.models import Artist
from django.db.models import Count

class ArtistRepository(BaseRepository):
    model = Artist

    def get_top_artists(self, limit=10):
        return Artist.objects.annotate(filtered_song_count=Count('song')).order_by('-filtered_song_count')[:limit]

    def get_all_countries(self):
        return Artist.objects.exclude(country='').exclude(country__isnull=True).values_list('country', flat=True).distinct().order_by('country')
