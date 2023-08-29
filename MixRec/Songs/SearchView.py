from rest_framework.viewsets import ModelViewSet
from django.db import transaction
from django.conf import settings

from .Decorators import catch_exceptions
from .Serializer import SongSerializer
from .models import Song
from .Index import Index

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances, manhattan_distances
from gensim import corpora, models, similarities

from nltk.stem import PorterStemmer

import joblib


def adjust_key_score(song_key, preferred_key):
    key_diff = (int(song_key[0])) - (int(preferred_key[0])) % 12
    return -0.08 * key_diff + 0.20


def calculate_key_scores(songs: [], scores: [float], preferred_key) -> list:
    adjusted_scores = []
    for song, score in zip(songs, scores):
        adjusted_scores.append(score + adjust_key_score(song.camelot_key, preferred_key))

    return adjusted_scores


class SearchEP(ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    @catch_exceptions
    def create(self, request, *args, **kwargs):
        query = request.data.get("query", None)
        method = request.data.get("method", "TF-IDF")
        k = int(request.data.get("k", 10))
        if query is None:
            raise Exception("No query provided")

        # preprocess query
        stemmer = PorterStemmer()
        query = " ".join([stemmer.stem(word) for word in query.split()])

        # index
        index: Index = joblib.load(settings.INDEX_PATH)
        song_ids = []
        scores = []
        if method == "TF-IDF":        # process query
            tfidf_query = index.vectorizer.transform([query])

            similarity_method = request.data.get("similarity_method", "Cosine")
            related_docs_indices = []
            scores = []
            if similarity_method == "Cosine":
                sims = cosine_similarity(tfidf_query, index.tfidf_matrix).flatten()
                related_docs_indices = sims.argsort()[:-k - 1:-1]
                scores = sims[related_docs_indices].tolist()

            elif similarity_method == "Euclidean":
                sims = euclidean_distances(tfidf_query, index.tfidf_matrix).flatten()
                related_docs_indices = sims.argsort()[:k]
                scores = sims[related_docs_indices].tolist()

            elif similarity_method == "Manhattan":
                sims = manhattan_distances(tfidf_query, index.tfidf_matrix).flatten()
                related_docs_indices = sims.argsort()[:k]
                scores = sims[related_docs_indices].tolist()

            # get song ids
            song_ids = [index.song_ids[i] for i in related_docs_indices]

        elif method == "LSI":
            query_bow = index.dictionary.doc2bow(query.lower().split())
            query_lsi = index.lsi_model[query_bow]
            similars = index.lsi_index[query_lsi]
            top_k = sorted(enumerate(similars), key=lambda item: -item[1])[:k]
            song_ids = [index.song_ids[i[0]] for i in top_k]
            scores = [i[1] for i in top_k]
        else:
            raise Exception("Invalid method")

        # get songs
        songs = Song.objects.filter(song_id__in=song_ids)

        # adjust scores for given key preference
        key = request.data.get("key", 'None')
        if key != 'None':
            scores = calculate_key_scores(songs, scores, key)

        response: dict = {
            "Songs": SongSerializer(songs, many=True, context={'request': request}).data,
            "Scores": scores
        }
        return response
