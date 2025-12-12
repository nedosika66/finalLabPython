from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from music_app.repositories import UnitOfWork
from web.forms import SongForm
import logging
from django.db.models import Q 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

logger = logging.getLogger('web')
uow = UnitOfWork()

PAGINATE_BY = 25

def _filter_and_get_songs_qs(query):
    songs_qs = uow.songs.model.objects.all()
    if query:
        songs_qs = songs_qs.filter(
            Q(title__icontains=query) |
            Q(main_artist__nickname__icontains=query)
        )
    return songs_qs.select_related('main_artist', 'album')

def song_list(request):
    sort_by = request.GET.get('sort', 'id')
    order = request.GET.get('order', 'asc')
    query = request.GET.get('q', '').strip()

    songs_qs = _filter_and_get_songs_qs(query)
    songs = list(songs_qs) 

    sort_map = {
        'id': lambda x: x.pk,
        'title': lambda x: x.title.lower() if x.title else "",
        'artist': lambda x: x.main_artist.nickname.lower() if x.main_artist else "",
        'album': lambda x: x.album.title.lower() if x.album else "",
        'year': lambda x: x.release_year if x.release_year else 0,
        'duration': lambda x: x.duration if x.duration else 0
    }

    if sort_by not in sort_map:
        sort_by = 'id'
    key_func = sort_map[sort_by]
    reverse = (order == 'desc')

    if sort_by in ['title', 'artist', 'album']:
        letters, others = [], []
        for s in songs:
            val = str(key_func(s)).strip()
            if val and val[0].isalpha():
                letters.append(s)
            else:
                others.append(s)
        letters.sort(key=key_func, reverse=reverse)
        others.sort(key=key_func, reverse=reverse)
        songs = letters + others
    else:
        songs.sort(key=key_func, reverse=reverse)
    
    page = request.GET.get('page', 1)
    paginator = Paginator(songs, PAGINATE_BY)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
        
    return render(request, 'web/song_list.html', {
        'songs': page_obj.object_list,
        'page_obj': page_obj,
        'current_sort': sort_by,
        'current_order': order,
        'query': query
    })


def song_detail(request, pk):
    song = uow.songs.get_by_id(pk)
    if not song: raise Http404()
    return render(request, 'web/song_detail.html', {'song': song})

@login_required
def song_edit(request, pk=None):
    if pk:
        song = uow.songs.get_by_id(pk)
        if not song: raise Http404()
    else: song = None
    if request.method == "POST":
        form = SongForm(request.POST, instance=song)
        if form.is_valid():
            song_obj = form.save(commit=False)
            if not pk: uow.songs.add(song_obj)
            else: uow.songs.update(pk, **form.cleaned_data)
            return redirect('song_detail', pk=song_obj.pk)
    else: form = SongForm(instance=song)
    return render(request, 'web/song_form.html', {'form': form})

@login_required
def song_delete(request, pk):
    song = uow.songs.get_by_id(pk)
    if not song: raise Http404()
    if request.method == "POST":
        uow.songs.delete(pk)
        return redirect('song_list')
    return render(request, 'web/song_confirm_delete.html', {'song': song})