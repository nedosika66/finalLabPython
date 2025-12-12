from .base_repository import BaseRepository
from music_app.models import Song

class SongRepository(BaseRepository):
    def __init__(self):
        super().__init__(Song)
