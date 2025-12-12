# music_app/serializers.py
from rest_framework import serializers
from .models import (
    Artist, Genre, Album, Song, Producer, StreamingPlatform, 
    AlbumArtist, SongProducer, SongFeature, SongAvailability
)

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'

class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = '__all__'

class StreamingPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamingPlatform
        fields = '__all__'

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'

class AlbumArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumArtist
        fields = '__all__'

class SongProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongProducer
        fields = '__all__'

class SongFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongFeature
        fields = '__all__'

class SongAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SongAvailability
        fields = '__all__'