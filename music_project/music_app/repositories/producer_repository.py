from .base_repository import BaseRepository
from music_app.models import Producer

class ProducerRepository(BaseRepository):
    def __init__(self):
        super().__init__(Producer)
