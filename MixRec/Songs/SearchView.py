from rest_framework.viewsets import ModelViewSet
from django.db import transaction
from django.conf import settings

from .Decorators import catch_exceptions
from .Serializer import SongSerializer
from .models import Song

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import joblib


class Index:
    def __init__(self):
        self.concatenations: [str] = []
        self.song_ids = []
        self.vectorizer = TfidfVectorizer(analyzer='word', stop_words='english', lowercase=True)
        self.tfidf_matrix = None


class SearchEP(ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    @catch_exceptions
    def create(self, request, *args, **kwargs):
        # Will recreate the search index for all songs
        response: dict = {}

        # collect artist, title, album, genre, description from the songs and put them in a single string
        songs = Song.objects.all()
        new_index = Index()
        for song in songs:
            new_index.concatenations.append(song.artist + " " + song.title + " " + song.album + " " + song.genre + " " + song.description + " " + song.camelot_key)
            new_index.song_ids.append(song.song_id)

        new_index.tfidf_matrix = new_index.vectorizer.fit_transform(new_index.concatenations)

        # save tf-idf matrix
        joblib.dump(new_index, settings.INDEX_PATH)

        return response

    @catch_exceptions
    def retrieve(self, request, *args, **kwargs):
        query = kwargs.get("pk", None)
        k = request.data.get("k", 10)
        if query is None:
            raise Exception("No query provided")

        # load tf-idf matrix
        index: Index = joblib.load(settings.INDEX_PATH)

        # process query
        tfidf_query = index.vectorizer.transform([query])

        # calculate cosine similarity
        cosine_similarities = linear_kernel(tfidf_query, index.tfidf_matrix).flatten()

        # get top k results
        related_docs_indices = cosine_similarities.argsort()[:-k-1:-1]

        # get song ids
        song_ids = [index.song_ids[i] for i in related_docs_indices]

        # get songs
        songs = Song.objects.filter(song_id__in=song_ids)
        for song in songs:
            print(song.artist + " - " + song.title)

        response: dict = {
            "Songs": SongSerializer(songs, many=True, context={'request': request}).data,
            "score": cosine_similarities[related_docs_indices].tolist()
        }
        return response
