from music_app.models import Platform

class PlatformRepository:
    def get_all(self):
        return Platform.objects.all()
