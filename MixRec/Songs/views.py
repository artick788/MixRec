from rest_framework.viewsets import ModelViewSet
from django.db import transaction
from django.conf import settings

from .Decorators import catch_exceptions
from .Serializer import SongSerializer
from .models import Song
from .Downloader import download_youtube
from .TunebatScraper import get_tunebat_data
import os
import taglib


class SongEP(ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    @catch_exceptions
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        artist = request.data["artist"]
        title = request.data["title"]
        album = request.data["album"]
        genre = request.data["genre"]
        description = request.data["description"]

        option = request.data.get("option", None)
        if option == "download":
            # first, extract all request data
            url = request.data["url"]

            # check file and create name
            if os.path.exists(settings.MUSIC_DIR):
                # sort music by genre
                if genre not in os.listdir(settings.MUSIC_DIR):
                    os.mkdir(settings.MUSIC_DIR + "/" + genre)
                file_name = settings.MUSIC_DIR + "/" + genre + "/" + artist + " - " + title + ".mp3"
                if os.path.isfile(file_name):
                    raise Exception("File already exists")

                # download file
                download_youtube(url, file_name)
            else:
                raise Exception("Music directory does not exist")
        elif option == "upload":
            pass

        else:
            raise Exception("Invalid option")

        # get song attributes
        info: dict = get_tunebat_data(artist, title)

        # fill MP3 metadata
        f = taglib.File(file_name)
        f.tags["ARTIST"] = artist
        f.tags["TITLE"] = title
        f.tags["ALBUM"] = album
        f.tags["GENRE"] = genre
        f.tags["BPM"] = info['BPM']
        f.tags["TKEY"] = info['Key']
        f.save()

        # create song object
        new_song: Song = Song.objects.create(file_location=file_name,
                                             title=title,
                                             artist=artist,
                                             album=album,
                                             description=description,
                                             genre=genre,
                                             duration=info['Duration'],
                                             key=info['Key'],
                                             camelot_key=info['Camelot'],
                                             bpm=int(info['BPM']),
                                             popularity=float(info['Popularity']),
                                             energy=float(info['Energy']),
                                             danceability=float(info['Danceability']),
                                             happiness=float(info['Happiness']),
                                             acousticness=float(info['Acousticness']),
                                             instrumentalness=float(info['Instrumentalness']),
                                             liveness=float(info['Liveness']),
                                             speechiness=float(info['Speechiness']),
                                             )
        new_song.save()

        # serialize and return
        song_serialized = SongSerializer(new_song, context={'request': request})
        response: dict = dict()
        response['Song'] = song_serialized.data
        return response

