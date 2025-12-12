from .base_repository import BaseRepository
from music_app.models import Song
from django.db.models import Count, Avg
from music_app.models import Genre, Artist

class SongRepository(BaseRepository):
    model = Song

    def get_statistics(self, queryset=None):
        qs = queryset or self.get_all()
        total_songs = qs.count()
        avg_duration = qs.aggregate(avg_duration=Avg('duration'))['avg_duration'] or 0
        return {'total_songs': total_songs, 'avg_duration': avg_duration}
    
    def get_all_genres(self):
        return Genre.objects.all().values_list('name', flat=True)

    def _get_all_countries():
        return list(Artist.objects.values_list('country', flat=True).distinct())