from music_app.repositories import UnitOfWork
import pandas as pd
import datetime
from django.db.models import Q, Count

uow = UnitOfWork()

def process_top_10(df, label_col, value_col):
    if df.empty:
        return df
    df = df.dropna(subset=[label_col])
    ignore = ['Unknown', 'unknown', '', 'None', 'nan']
    df = df[~df[label_col].astype(str).isin(ignore)]
    return df.sort_values(by=value_col, ascending=False).head(10)

def get_aggregated_data(min_year=None, max_year=None, genre_filter=None, country_filter=None):
    filters = {}
    if min_year:
        filters['release_year__gte'] = min_year
    if max_year:
        filters['release_year__lte'] = max_year
    if genre_filter:
        filters['genre__name'] = genre_filter
    if country_filter:
        filters['main_artist__country'] = country_filter

    songs_qs = uow.songs.filter_by(**filters)

    qs_genres = songs_qs.values('genre__name').annotate(total_songs=Count('pk')).order_by('-total_songs')
    df_genres = process_top_10(pd.DataFrame(list(qs_genres)), 'genre__name', 'total_songs')

    raw_years = list(songs_qs.values('release_year', 'duration'))
    df_years = pd.DataFrame(raw_years)

    if not df_years.empty and 'duration' in df_years.columns:
        def parse_duration(val):
            if val is None:
                return 0.0
            if isinstance(val, datetime.timedelta):
                return val.total_seconds() / 60.0
            if isinstance(val, datetime.time):
                return (val.hour * 3600 + val.minute * 60 + val.second) / 60.0
            try:
                return float(val) / 60.0
            except:
                return 0.0

        df_years['avg_duration'] = df_years['duration'].apply(parse_duration)
        df_years = df_years.groupby('release_year')['avg_duration'].mean().reset_index()
        df_years['avg_duration'] = df_years['avg_duration'].round(2)
        df_years = df_years.sort_values('release_year')
    else:
        df_years = pd.DataFrame(columns=['release_year', 'avg_duration'])

    artists_qs = uow.artists.model.objects.filter(song__in=songs_qs).values('nickname').annotate(filtered_song_count=Count('song')).order_by('-filtered_song_count')
    df_artists = pd.DataFrame(list(artists_qs))
    df_artists = process_top_10(df_artists, 'nickname', 'filtered_song_count') if not df_artists.empty else pd.DataFrame()

    albums_qs = songs_qs.values('album__title').annotate(filtered_track_count=Count('pk')).order_by('-filtered_track_count')
    df_albums = pd.DataFrame(list(albums_qs))
    df_albums = process_top_10(df_albums, 'album__title', 'filtered_track_count') if not df_albums.empty else pd.DataFrame()

    countries_qs = uow.artists.model.objects.filter(song__in=songs_qs).distinct().values('country').annotate(artist_count=Count('pk')).order_by('-artist_count')
    df_countries = pd.DataFrame(list(countries_qs))
    df_countries = process_top_10(df_countries, 'country', 'artist_count') if not df_countries.empty else pd.DataFrame()

    producers_qs = songs_qs.values('producers__nickname').annotate(filtered_prod_count=Count('pk')).order_by('-filtered_prod_count')
    df_producers = pd.DataFrame(list(producers_qs))
    df_producers = process_top_10(df_producers, 'producers__nickname', 'filtered_prod_count') if not df_producers.empty else pd.DataFrame()

    return {
        'genres_df': df_genres,
        'years_df': df_years,
        'artists_df': df_artists,
        'albums_df': df_albums,
        'countries_df': df_countries,
        'producers_df': df_producers
    }

def get_song_statistics():
    songs = uow.songs.get_all()
    minutes_list = []

    for s in songs:
        if s.duration:
            val = s.duration
            if isinstance(val, datetime.timedelta):
                minutes_list.append(val.total_seconds() / 60.0)
            elif isinstance(val, datetime.time):
                minutes_list.append((val.hour * 3600 + val.minute * 60 + val.second) / 60.0)

    if not minutes_list:
        return {'mean': 0, 'median': 0, 'min': 0, 'max': 0}

    series = pd.Series(minutes_list)
    return {
        'mean': round(series.mean(), 2),
        'median': round(series.median(), 2),
        'min': round(series.min(), 2),
        'max': round(series.max(), 2)
    }
