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


class IntegrityEP(ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    @catch_exceptions
    def list(self, request, *args, **kwargs):
        songs = Song.objects.all()
        missing_songs = []
        for song in songs:
            print("Checking " + song.file_location)
            if not os.path.isfile(song.file_location):
                missing_songs.append(song)
            else:
                f = taglib.File(song.file_location)
                f.tags["ARTIST"] = song.artist
                f.tags["TITLE"] = song.title
                f.tags["ALBUM"] = song.album
                f.tags["GENRE"] = song.genre
                f.tags["COMMENT"] = song.description
                f.tags["BPM"] = str(song.bpm)
                f.tags["TKEY"] = song.key
                f.save()

        response: dict = {
            "missing_songs": SongSerializer(missing_songs, many=True, context={"request": request}).data
        }
        return response
