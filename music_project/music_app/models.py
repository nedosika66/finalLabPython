from django.db import models

class Artist(models.Model):
    artist_id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=50, unique=True)
    real_name = models.CharField(max_length=100)
    birth_year = models.PositiveIntegerField()
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    listeners = models.IntegerField(default=0)

    class Meta:
        db_table = 'artist'

    def __str__(self):
        return self.nickname
    

class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    origin_city = models.CharField(max_length=50, blank=True, null=True)
    origin_country = models.CharField(max_length=50, blank=True, null=True)
    origin_year = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'genre'

    def __str__(self):
        return self.name


class Album(models.Model):
    album_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    release_year = models.PositiveIntegerField()
    total_songs = models.IntegerField(default=0)
    label = models.CharField(max_length=50, blank=True, null=True)
    artists = models.ManyToManyField('Artist', through='AlbumArtist')

    class Meta:
        db_table = 'album'

    def __str__(self):
        return self.title


class AlbumArtist(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    class Meta:
        db_table = 'album_artist'


class Producer(models.Model):
    producer_id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=50, unique=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    birth_year = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'producer'

    def __str__(self):
        return self.nickname


class Song(models.Model):
    song_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    duration = models.TimeField(blank=True, null=True)
    release_year = models.PositiveIntegerField()
    main_artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)
    producers = models.ManyToManyField('Producer', through='SongProducer')
    features = models.ManyToManyField(Artist, through='SongFeature', related_name='featured_songs')
    availability = models.ManyToManyField('StreamingPlatform', through='SongAvailability')

    class Meta:
        db_table = 'song'

    def __str__(self):
        return self.title


class SongProducer(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)

    class Meta:
        db_table = 'song_producer'


class SongFeature(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    class Meta:
        db_table = 'song_feature'


class StreamingPlatform(models.Model):
    platform_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'streaming_platform'

    def __str__(self):
        return self.name


class SongAvailability(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    platform = models.ForeignKey(StreamingPlatform, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=False)

    class Meta:
        db_table = 'song_availability'


class Platform(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
