import os
import sys
import django
from datetime import timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "music_project.settings")
django.setup()

from music_app.repositories import UnitOfWork
from music_app.models import Artist, Album, Song, Genre

uow = UnitOfWork()

def menu_artists():
    while True:
        print("\n==== Artists Menu ====")
        print("1. Показати всіх артистів")
        print("2. Додати нового артиста")
        print("3. Оновити артиста")
        print("4. Видалити артиста")
        print("5. Пошук артиста за нікнеймом")
        print("6. Показати пісні артиста")
        print("0. Назад")
        choice = input("Виберіть дію: ")

        if choice == "1":
            artists = uow.artists.get_all()
            if not artists:
                print("У базі немає артистів.")
            else:
                for a in artists:
                    print(f"{a.artist_id}: {a.nickname} ({a.real_name}) - {a.country}, слухачів: {a.listeners}")
        elif choice == "2":
            nickname = input("Нікнейм: ")
            real_name = input("Справжнє ім'я: ")
            birth_year = int(input("Рік народження: "))
            country = input("Країна: ")
            artist = Artist(nickname=nickname, real_name=real_name, birth_year=birth_year, country=country)
            uow.artists.add(artist)
            print("Артиста додано:", artist)
        elif choice == "3":
            artist_id = int(input("ID артиста для оновлення: "))
            new_nick = input("Новий нікнейм (залиште порожнім, якщо не змінювати): ")
            kwargs = {}
            if new_nick:
                kwargs["nickname"] = new_nick
            updated = uow.artists.update(artist_id, **kwargs)
            if updated:
                print("Оновлено:", updated)
            else:
                print("Артист не знайдений")
        elif choice == "4":
            artist_id = int(input("ID артиста для видалення: "))
            deleted = uow.artists.delete(artist_id)
            print("Видалено" if deleted else "Артист не знайдений")
        elif choice == "5":
            nickname = input("Нікнейм для пошуку: ")
            artist = uow.artists.get_by_field("nickname", nickname)
            if artist:
                print(f"Знайдено: {artist.artist_id}: {artist.nickname} ({artist.real_name}), {artist.country}, слухачів: {artist.listeners}")
            else:
                print("Артист не знайдений")
        elif choice == "6":
            artist_id = int(input("ID артиста: "))
            songs = Song.objects.filter(main_artist_id=artist_id)
            if songs:
                for s in songs:
                    print(f"{s.song_id}: {s.title} ({s.release_year})")
            else:
                print("Пісень не знайдено")
        elif choice == "0":
            break
        else:
            print("Невірний вибір, спробуйте ще раз.")

def menu_analytics():
    while True:
        print("\n==== Analytics Menu ====")
        print("1. Середня кількість слухачів артистів")
        print("2. Кількість пісень по жанрах")
        print("3. Середня кількість пісень в альбомах")
        print("4. Середній рік випуску по жанрах")
        print("5. Середня тривалість пісень")
        print("6. Найдовші та найкоротші пісні")
        print("0. Назад")
        choice = input("Виберіть дію: ")

        if choice == "1":
            artists = uow.artists.get_all()
            if artists:
                avg_listeners = sum(a.listeners for a in artists) / len(artists)
                print(f"Середня кількість слухачів: {avg_listeners:.0f}")
            else:
                print("Артисти відсутні")
        elif choice == "2":
            genres = uow.genres.get_all()
            for g in genres:
                songs_count = Song.objects.filter(genre=g).count()
                print(f"{g.name}: {songs_count} пісень")
        elif choice == "3":
            albums = uow.albums.get_all()
            if albums:
                avg_songs = sum(a.total_songs for a in albums) / len(albums)
                print(f"Середня кількість пісень в альбомах: {avg_songs:.1f}")
            else:
                print("Альбоми відсутні")
        elif choice == "4":
            genres = uow.genres.get_all()
            for g in genres:
                songs = Song.objects.filter(genre=g)
                if songs:
                    avg_year = sum(s.release_year for s in songs) / songs.count()
                    print(f"{g.name}: середній рік випуску {avg_year:.0f}")
                else:
                    print(f"{g.name}: пісень немає")
        elif choice == "5":
            songs = uow.songs.get_all()
            if songs:
                total_seconds = sum(
                    s.duration.hour * 3600 + s.duration.minute * 60 + s.duration.second
                    for s in songs if s.duration
                )
                avg_seconds = total_seconds / songs.count()
                avg_time = timedelta(seconds=int(avg_seconds))
                print(f"Середня тривалість пісень: {str(avg_time)}")
            else:
                print("Пісень немає")
        elif choice == "6":
            songs = [s for s in uow.songs.get_all() if s.duration]
            if songs:
                longest = max(songs, key=lambda s: s.duration)
                shortest = min(songs, key=lambda s: s.duration)
                print(f"Найдовша пісня: {longest.title} ({longest.duration})")
                print(f"Найкоротша пісня: {shortest.title} ({shortest.duration})")
            else:
                print("Пісень немає")
        elif choice == "0":
            break
        else:
            print("Невірний вибір, спробуйте ще раз.")

def main_menu():
    while True:
        print("\n==== Music DB CLI ====")
        print("1. Робота з артистами")
        print("2. Аналітика")
        print("0. Вихід")
        choice = input("Виберіть дію: ")

        if choice == "1":
            menu_artists()
        elif choice == "2":
            menu_analytics()
        elif choice == "0":
            break
        else:
            print("Невірний вибір")

if __name__ == "__main__":
    main_menu()
