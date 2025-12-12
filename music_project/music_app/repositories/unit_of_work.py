from .song_repository import SongRepository
from .artist_repository import ArtistRepository
from .album_repository import AlbumRepository
from .producer_repository import ProducerRepository
from .genre_repository import GenreRepository
from .platform_repository import PlatformRepository
from .analytics_repository import AnalyticsRepository

class UnitOfWork:
    def __init__(self):
        self.songs = SongRepository()
        self.artists = ArtistRepository()
        self.albums = AlbumRepository()
        self.producers = ProducerRepository()
        self.genres = GenreRepository()
        self.platforms = PlatformRepository()
        self.analytics = AnalyticsRepository()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
