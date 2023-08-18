from django.db import models
import uuid


class Song(models.Model):
    song_id = models.UUIDField(editable=False, null=False, default=uuid.uuid4, verbose_name="UUID")
    added_at = models.DateTimeField(auto_now_add=True)
    file_location = models.CharField(max_length=512, null=True, blank=True)

    title = models.CharField(max_length=512, null=False, blank=False)
    artist = models.CharField(max_length=512, null=False, blank=False)
    album = models.CharField(max_length=512, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    genre = models.CharField(max_length=512, null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)

    key = models.CharField(max_length=4, null=True, blank=True)
    camelot_key = models.CharField(max_length=4, null=True, blank=True)
    bpm = models.IntegerField(null=True, blank=True, default=0)
    popularity = models.FloatField(null=True, blank=True, default=0.0)
    energy = models.FloatField(null=True, blank=True, default=0.0)
    danceability = models.FloatField(null=True, blank=True, default=0.0)
    happiness = models.FloatField(null=True, blank=True, default=0.0)
    acousticness = models.FloatField(null=True, blank=True, default=0.0)
    instrumentalness = models.FloatField(null=True, blank=True, default=0.0)
    liveness = models.FloatField(null=True, blank=True, default=0.0)
    speechiness = models.FloatField(null=True, blank=True, default=0.0)

    def __str__(self):
        return str(self.song_id) + " - " + str(self.title) + " by " + str(self.artist)


