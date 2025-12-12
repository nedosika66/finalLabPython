from django.shortcuts import render
from django.http import Http404
from music_app.repositories import UnitOfWork
from django.db.models import Avg, Count, Q

uow = UnitOfWork()

def _get_artist_detail_data(pk):
    try:
        artist = uow.artists.get_by_id(pk)
    except Exception: 
        artist = None
    if not artist: return None
    
    albums = artist.album_set.all() 
    songs_qs = artist.song_set.filter(main_artist=artist).order_by('album__release_year', 'album__title', 'title') 

    return {
        'artist': artist,
        'albums': albums,
        'songs': songs_qs,
        'total_songs': songs_qs.count(),
        'total_albums': albums.count(),
        'avg_duration': songs_qs.aggregate(Avg('duration'))['duration__avg']
    }

def artist_detail(request, pk):
    detail_data = _get_artist_detail_data(pk)
    if not detail_data:
        raise Http404("Виконавця не знайдено")

    return render(request, 'web/artist_detail.html', detail_data)

def _filter_and_get_artists_qs(query):
    artists_qs = uow.artists.model.objects.annotate(num_songs=Count('song'))
    
    if query:
        artists_qs = artists_qs.filter(
            Q(nickname__icontains=query) |
            Q(real_name__icontains=query)
        )
    return artists_qs


def artist_list(request):
    sort_by = request.GET.get('sort', 'nickname')
    order = request.GET.get('order', 'asc')
    query = request.GET.get('q', '').strip()

    artists_qs = _filter_and_get_artists_qs(query)
    artists = list(artists_qs)

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