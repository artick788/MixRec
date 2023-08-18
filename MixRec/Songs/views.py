from rest_framework.viewsets import ModelViewSet
from django.db import transaction

from .Decorators import catch_exceptions
from .Serializer import SongSerializer
from .models import Song


class SongEP(ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    @catch_exceptions
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        pass

