from music_app.models import Song
from django.db.models import Count


class GenreRepository:
    def get_top_genres(self, queryset=None, limit=10):
        qs = queryset or Song.objects.all()
        return qs.values('genre__name').annotate(total_songs=Count('id')).order_by('-total_songs')[:limit]

    def get_all_genres(self):
        return Song.objects.values_list('genre__name', flat=True).distinct().order_by('genre__name')
