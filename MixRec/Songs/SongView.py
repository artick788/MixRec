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

        # check file and create name
        if os.path.exists(settings.MUSIC_DIR):
            # sort music by genre
            if genre not in os.listdir(settings.MUSIC_DIR):
                os.mkdir(settings.MUSIC_DIR + "\\" + genre)
            file_name = settings.MUSIC_DIR + "\\" + genre + "\\" + artist + " - " + title + ".mp3"
            if os.path.isfile(file_name):
                raise Exception("File already exists")
        else:
            raise Exception("Music directory does not exist")

        option = request.data.get("option", None)
        if option == "download":
            # first, extract all request data
            url = request.data["url"]

            # download file
            download_youtube(url, file_name)
        elif option == "upload":
            uploaded_file = request.FILES["file"]
            with open(file_name, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
        else:
            raise Exception("Invalid option")

        # get song attributes
        try:
            info: dict = get_tunebat_data(artist, title)
        except Exception as e:
            print("Failed to get song attributes: " + str(e))
            raise Exception("Failed to get song attributes: " + str(e))

        # fill MP3 metadata
        f = taglib.File(file_name)
        f.tags["ARTIST"] = artist
        f.tags["TITLE"] = title
        f.tags["ALBUM"] = album
        f.tags["GENRE"] = genre
        f.tags["COMMENT"] = description
        f.tags["BPM"] = info.get('BPM', "0")
        f.tags["TKEY"] = info.get('Key', "0")
        f.save()

        # create song object
        new_song: Song = Song.objects.create(file_location=file_name,
                                             title=title,
                                             artist=artist,
                                             album=album,
                                             description=description,
                                             genre=genre,
                                             duration=info.get('Duration', "0"),
                                             key=info.get('Key', ""),
                                             camelot_key=info.get('Camelot', ""),
                                             bpm=int(info.get('BPM', "")),
                                             popularity=float(info.get('Popularity', "")),
                                             energy=float(info.get('Energy', "")),
                                             danceability=float(info.get('Danceability', "")),
                                             happiness=float(info.get('Happiness', "")),
                                             acousticness=float(info.get('Acousticness', "")),
                                             instrumentalness=float(info.get('Instrumentalness', "")),
                                             liveness=float(info.get('Liveness', "")),
                                             speechiness=float(info.get('Speechiness', "")),
                                             )
        new_song.save()

        # serialize and return
        song_serialized = SongSerializer(new_song, context={'request': request})
        response: dict = dict()
        response['Song'] = song_serialized.data
        return response

    @catch_exceptions
    def partial_update(self, request, *args, **kwargs):
        song = Song.objects.get(song_id=kwargs['pk'])
        # if the genre is changed, move the file to the new genre folder
        if song.genre != request.data["genre"] or song.artist != request.data["artist"] or song.title != request.data["title"]:
            # update file on disk
            old_file_name = song.file_location
            new_file_name = settings.MUSIC_DIR + "\\" + request.data["genre"] + "\\" + request.data["artist"] + " - " + request.data["title"] + ".mp3"
            os.rename(old_file_name, new_file_name)
            song.file_location = new_file_name
            song.save()

            # update file metadata
            f = taglib.File(new_file_name)
            f.tags["ARTIST"] = request.data["artist"]
            f.tags["TITLE"] = request.data["title"]
            f.tags["GENRE"] = request.data["genre"]
            f.save()

        if song.description != request.data["description"]:
            f = taglib.File(song.file_location)
            f.tags["COMMENT"] = request.data["description"]
            f.save()
            song.description = request.data["description"]
            song.save()

        super().partial_update(request, *args, **kwargs)
        song = Song.objects.get(song_id=kwargs['pk'])
        song_serialized = SongSerializer(song, context={'request': request})
        response: dict = dict()
        response['Song'] = song_serialized.data
        return response

    @catch_exceptions
    def list(self, request, *args, **kwargs):
        response: dict = dict()
        response['Songs'] = SongSerializer(Song.objects.all(), many=True, context={'request': request}).data
        return response

