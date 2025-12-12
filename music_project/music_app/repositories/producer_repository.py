from music_app.models import Producer
from django.db.models import Count

class ProducerRepository:
    def get_top_producers(self, limit=10):
        return Producer.objects.annotate(filtered_prod_count=Count('song')).order_by('-filtered_prod_count')[:limit]
