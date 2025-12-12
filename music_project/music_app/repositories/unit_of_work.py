from .artist_repository import ArtistRepository
from .album_repository import AlbumRepository
from .song_repository import SongRepository
from .genre_repository import GenreRepository
from .producer_repository import ProducerRepository
from .platform_repository import StreamingPlatformRepository

class UnitOfWork:
    def __init__(self):
        self.artists = ArtistRepository()
        self.albums = AlbumRepository()
        self.songs = SongRepository()
        self.genres = GenreRepository()
        self.producers = ProducerRepository()
        self.platforms = StreamingPlatformRepository()
