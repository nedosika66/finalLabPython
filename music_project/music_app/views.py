from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .repositories import UnitOfWork
from .models import (
    Artist, Genre, Album, Song, Producer, StreamingPlatform
)
from .serializers import (
    ArtistSerializer, GenreSerializer, AlbumSerializer, 
    ProducerSerializer, StreamingPlatformSerializer, SongSerializer
)

uow = UnitOfWork()


def artists_view(request):
    artists = uow.artists.get_all()
    return render(request, "music_app/artists.html", {"artists": artists})

def songs_view(request):
    songs = uow.songs.get_all()
    return render(request, "music_app/songs.html", {"songs": songs})

class ArtistViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = uow.artists.get_all()
        serializer = ArtistSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid():
            new_artist = Artist(**serializer.validated_data)
            uow.artists.add(new_artist) 
            return Response(ArtistSerializer(new_artist).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        artist = uow.artists.get_by_id(pk)
        if artist:
            serializer = ArtistSerializer(artist)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        updated_artist = uow.artists.update(pk, **request.data)
        if updated_artist:
            serializer = ArtistSerializer(updated_artist)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        if uow.artists.delete(pk):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def listeners_report(self, request):
        report_data = uow.artists.get_listeners_report()
        return Response(report_data)


class GenreViewSet(viewsets.ViewSet):
    
    def list(self, request):
        queryset = uow.genres.get_all()
        serializer = GenreSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            new_obj = Genre(**serializer.validated_data)
            uow.genres.add(new_obj)
            return Response(GenreSerializer(new_obj).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        obj = uow.genres.get_by_id(pk)
        if obj:
            serializer = GenreSerializer(obj)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        obj = uow.genres.update(pk, **request.data)
        if obj:
            serializer = GenreSerializer(obj)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        if uow.genres.delete(pk):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class AlbumViewSet(viewsets.ViewSet):
    
    def list(self, request):
        queryset = uow.albums.get_all()
        serializer = AlbumSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = AlbumSerializer(data=request.data)
        if serializer.is_valid():
            new_obj = Album(**serializer.validated_data)
            uow.albums.add(new_obj)
            return Response(AlbumSerializer(new_obj).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        obj = uow.albums.get_by_id(pk)
        if obj:
            serializer = AlbumSerializer(obj)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        obj = uow.albums.update(pk, **request.data)
        if obj:
            serializer = AlbumSerializer(obj)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        if uow.albums.delete(pk):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class SongViewSet(viewsets.ViewSet):
    
    def list(self, request):
        queryset = uow.songs.get_all()
        serializer = SongSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid():
            new_obj = Song(**serializer.validated_data)
            uow.songs.add(new_obj)
            return Response(SongSerializer(new_obj).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        obj = uow.songs.get_by_id(pk)
        if obj:
            serializer = SongSerializer(obj)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        obj = uow.songs.update(pk, **request.data)
        if obj:
            serializer = SongSerializer(obj)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        if uow.songs.delete(pk):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class ProducerViewSet(viewsets.ViewSet):
    
    def list(self, request):
        queryset = uow.producers.get_all()
        serializer = ProducerSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProducerSerializer(data=request.data)
        if serializer.is_valid():
            new_obj = Producer(**serializer.validated_data)
            uow.producers.add(new_obj)
            return Response(ProducerSerializer(new_obj).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        obj = uow.producers.get_by_id(pk)
        if obj:
            serializer = ProducerSerializer(obj)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        obj = uow.producers.update(pk, **request.data)
        if obj:
            serializer = ProducerSerializer(obj)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        if uow.producers.delete(pk):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class StreamingPlatformViewSet(viewsets.ViewSet):
    
    def list(self, request):
        queryset = uow.platforms.get_all()
        serializer = StreamingPlatformSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = StreamingPlatformSerializer(data=request.data)
        if serializer.is_valid():
            new_obj = StreamingPlatform(**serializer.validated_data)
            uow.platforms.add(new_obj)
            return Response(StreamingPlatformSerializer(new_obj).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        obj = uow.platforms.get_by_id(pk)
        if obj:
            serializer = StreamingPlatformSerializer(obj)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        obj = uow.platforms.update(pk, **request.data)
        if obj:
            serializer = StreamingPlatformSerializer(obj)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        if uow.platforms.delete(pk):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)