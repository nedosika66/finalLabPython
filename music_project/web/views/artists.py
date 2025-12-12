from django.shortcuts import render
from django.http import Http404
from django.db.models import Avg, Count
from music_app.models import Artist, Song, Album

def artist_detail(request, pk):
    try:
        artist = Artist.objects.get(pk=pk)
    except Artist.DoesNotExist:
        raise Http404("Виконавця не знайдено")

    albums = Album.objects.filter(artists=artist)
    songs = Song.objects.filter(main_artist=artist).order_by('album__release_year', 'album__title', 'title')

    context = {
        'artist': artist,
        'albums': albums,
        'songs': songs,
        'total_songs': songs.count(),
        'total_albums': albums.count(),
        'avg_duration': songs.aggregate(Avg('duration'))['duration__avg']
    }
    return render(request, 'web/artist_detail.html', context)

def artist_list(request):
    sort_by = request.GET.get('sort', 'nickname')
    order = request.GET.get('order', 'asc')
    query = request.GET.get('q', '').strip()

    artists = list(
        Artist.objects.annotate(num_songs=Count('song'))
    )

    if query:
        artists = [
            a for a in artists
            if query.lower() in (a.nickname or "").lower()
            or query.lower() in (a.real_name or "").lower()
        ]

    sort_map = {
        'id': lambda x: x.pk,
        'nickname': lambda x: x.nickname.lower() if x.nickname else "",
        'real_name': lambda x: x.real_name.lower() if x.real_name else "",
        'country': lambda x: x.country.lower() if x.country else "",
        'songs': lambda x: x.num_songs
    }

    if sort_by not in sort_map:
        sort_by = 'nickname'

    key_func = sort_map[sort_by]
    reverse = (order == 'desc')

    text_fields = ['nickname', 'real_name', 'country']

    if sort_by in text_fields:
        letters = []
        others = []

        for artist in artists:
            val = key_func(artist)
            s_val = str(val).strip()

            if s_val and s_val[0].isalpha():
                letters.append(artist)
            else:
                others.append(artist)

        letters.sort(key=key_func, reverse=reverse)
        others.sort(key=key_func, reverse=reverse)

        artists = letters + others

    else:
        artists.sort(key=key_func, reverse=reverse)

    context = {
        'artists': artists,
        'current_sort': sort_by,
        'current_order': order,
        'query': query
    }
    return render(request, 'web/artist_list.html', context)
