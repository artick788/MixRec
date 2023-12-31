from django.urls import path
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from .SongView import SongEP
from .SearchView import SearchEP
from .IndexView import IndexEP
from .IntegrityView import IntegrityEP

router = DefaultRouter()
router.register(r'song', SongEP, 'song')
router.register(r'search', SearchEP, 'search')
router.register(r'index', IndexEP, 'index')
router.register(r'integrity', IntegrityEP, 'integrity')
