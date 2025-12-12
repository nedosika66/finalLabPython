# music_app/urls_api.py
from rest_framework.routers import DefaultRouter
from .views import (
    ArtistViewSet, GenreViewSet, AlbumViewSet, 
    SongViewSet, ProducerViewSet, StreamingPlatformViewSet
)

router = DefaultRouter()
router.register(r'artists', ArtistViewSet, basename='artist')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'albums', AlbumViewSet, basename='album')
router.register(r'songs', SongViewSet, basename='song')
router.register(r'producers', ProducerViewSet, basename='producer')
router.register(r'platforms', StreamingPlatformViewSet, basename='platform')

urlpatterns = router.urls