import pandas as pd
import datetime
from django.db.models import Count, Avg, Q
from music_app.models import Song, Artist, Album, Producer, Genre

class AnalyticsRepository:
    
    def _parse_duration(self, val):
        if val is None: return 0.0
        if isinstance(val, datetime.timedelta):
            return val.total_seconds() / 60.0
        if isinstance(val, datetime.time):
            return (val.hour * 3600 + val.minute * 60 + val.second) / 60.0
        try: return float(val) / 60.0
        except: return 0.0

    def _process_top_10(self, df, label_col, value_col):
        if df.empty: return df
        df = df.dropna(subset=[label_col])
        ignore = ['Unknown', 'unknown', '', 'None', 'nan']
        df = df[~df[label_col].astype(str).isin(ignore)]
        return df.sort_values(by=value_col, ascending=False).head(10)

    def get_all_genres(self):
        return list(Genre.objects.values_list('name', flat=True).distinct().order_by('name'))

    def get_all_countries(self):
        return list(Artist.objects.exclude(country='').exclude(country__isnull=True).values_list('country', flat=True).distinct().order_by('country'))

    def get_aggregated_data(self, min_year=None, max_year=None, genre_filter=None, country_filter=None):
        song_filter = Q()
        if min_year:
            song_filter &= Q(release_year__gte=min_year)
        if max_year:
            song_filter &= Q(release_year__lte=max_year)
        if genre_filter:
            song_filter &= Q(genre__name=genre_filter)
        if country_filter:
            song_filter &= Q(main_artist__country=country_filter)

        songs_qs = Song.objects.filter(song_filter) 

        qs_genres = songs_qs.values('genre__name').annotate(total_songs=Count('pk')).order_by('-total_songs')
        df_genres = self._process_top_10(pd.DataFrame(list(qs_genres)), 'genre__name', 'total_songs')

        raw_years = list(songs_qs.values('release_year', 'duration'))
        df_years = pd.DataFrame(raw_years)
        
        if not df_years.empty and 'duration' in df_years.columns:
            df_years['avg_duration'] = df_years['duration'].apply(self._parse_duration)
            df_years = df_years.groupby('release_year')['avg_duration'].mean().reset_index()
            df_years['avg_duration'] = df_years['avg_duration'].round(2)
            df_years = df_years.sort_values('release_year')
        else:
            df_years = pd.DataFrame(columns=['release_year', 'avg_duration'])

        qs_artists = Artist.objects.filter(song__in=songs_qs).values('nickname').annotate(filtered_song_count=Count('song')).order_by('-filtered_song_count')
        df_artists = self._process_top_10(pd.DataFrame(list(qs_artists)).rename(columns={'nickname': 'nickname'}), 'nickname', 'filtered_song_count')

        qs_albums = Album.objects.filter(song__in=songs_qs).values('title').annotate(filtered_track_count=Count('song')).order_by('-filtered_track_count')
        df_albums = self._process_top_10(pd.DataFrame(list(qs_albums)).rename(columns={'title': 'title'}), 'title', 'filtered_track_count')

        filtered_artists_qs = Artist.objects.filter(song__in=songs_qs).distinct()
        qs_countries = filtered_artists_qs.values('country').annotate(artist_count=Count('pk')).order_by('-artist_count')
        df_countries = self._process_top_10(pd.DataFrame(list(qs_countries)), 'country', 'artist_count')

        qs_producers = Producer.objects.filter(song__in=songs_qs).values('nickname').annotate(filtered_prod_count=Count('song')).order_by('-filtered_prod_count')
        df_producers = self._process_top_10(pd.DataFrame(list(qs_producers)).rename(columns={'nickname': 'nickname'}), 'nickname', 'filtered_prod_count')

        return {
            'genres_df': df_genres,
            'years_df': df_years,
            'artists_df': df_artists,
            'albums_df': df_albums,
            'countries_df': df_countries,
            'producers_df': df_producers
        }

    def get_song_statistics(self):
        songs = Song.objects.all() 
        minutes_list = []
        
        for s in songs:
            if s.duration:
                minutes_list.append(self._parse_duration(s.duration))
        
        if not minutes_list:
            stats = {'mean': 0, 'median': 0, 'min': 0, 'max': 0}
        else:
            series = pd.Series(minutes_list)
            stats = {
                'mean': round(series.mean(), 2),
                'median': round(series.median(), 2),
                'min': round(series.min(), 2),
                'max': round(series.max(), 2)
            }
        
        stats.update({
            'total_songs': Song.objects.count(),
            'total_artists': Artist.objects.count(),
            'total_albums': Album.objects.count(),
            'total_producers': Producer.objects.count()
        })
        return stats