from .base_repository import BaseRepository
from music_app.models import StreamingPlatform

class StreamingPlatformRepository(BaseRepository):
    def __init__(self):
        super().__init__(StreamingPlatform)
