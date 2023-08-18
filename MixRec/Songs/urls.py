from django.urls import path
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from .views import SongEP

router = DefaultRouter()
router.register(r'song', SongEP, 'song')