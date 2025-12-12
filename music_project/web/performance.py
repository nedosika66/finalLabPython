import time
import concurrent.futures
from django.db import connections
from music_app.models import Song

def run_simple_query():
    try:
        _ = list(Song.objects.all()[:50])
    finally:
        for conn in connections.all():
            conn.close()

def benchmark_threading(query_count=100, max_workers_list=[1, 2, 4, 8, 16]):
    results = []

    for workers in max_workers_list:
        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(run_simple_query) for _ in range(query_count)]
            concurrent.futures.wait(futures)

        end_time = time.time()
        duration = end_time - start_time

        results.append({
            'workers': workers,
            'time': round(duration, 4),
            'queries_per_sec': round(query_count / duration, 2)
        })

    return results
