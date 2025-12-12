from .base_repository import BaseRepository
from music_app.models import Genre

class GenreRepository(BaseRepository):
    def __init__(self):
        super().__init__(Genre)
