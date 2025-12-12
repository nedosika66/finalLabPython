from django.shortcuts import render
from music_app.models import Song, Artist, Album

def home(request):
    context = {
        'total_songs': Song.objects.count(),
        'total_artists': Artist.objects.count(),
        'total_albums': Album.objects.count(),
    }
    return render(request, 'web/index.html', context)