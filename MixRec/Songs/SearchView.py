from rest_framework.viewsets import ModelViewSet
from django.db import transaction
from django.conf import settings

from .Decorators import catch_exceptions
from .Serializer import SongSerializer
from .models import Song

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from gensim import corpora, models, similarities

import joblib


class Index:
    def __init__(self):
        self.concatenations: [str] = []
        self.tokenized_concatenations: [[str]] = []
        self.song_ids = []
        # for TF.IDF calculation
        self.vectorizer = TfidfVectorizer(analyzer='word', stop_words='english', lowercase=True)
        self.tfidf_matrix = None
        # for LSI calculation
        self.dictionary = None      # for mapping between words and their integer ids
        self.lsi_model = None       # for LSI calculation
        self.lsi_index = None      # for dimensionality reduction


"""
The biggest bullshit ever. As it is seemingly impossible to provide data using a get request, I have to use a post request.
To create the index, we dont need any data, so we switched the requests from place. To create the index, we now use a get
and to retrieve songs, we use a post. This is the only way to make it work.
"""
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

        # index
        index: Index = joblib.load(settings.INDEX_PATH)
        song_ids = []
        scores = []
        if method == "TF-IDF":        # process query
            tfidf_query = index.vectorizer.transform([query])

            # calculate cosine similarity
            cosine_similarities = linear_kernel(tfidf_query, index.tfidf_matrix).flatten()

            # get top k results
            related_docs_indices = cosine_similarities.argsort()[:-k - 1:-1]

            # get song ids
            song_ids = [index.song_ids[i] for i in related_docs_indices]
            scores = cosine_similarities[related_docs_indices].tolist()

        elif method == "LSI":
            query_bow = index.dictionary.doc2bow(query.lower().split())
            query_lsi = index.lsi_model[query_bow]
            similars = index.lsi_index[query_lsi]
            top_k = sorted(enumerate(similars), key=lambda item: -item[1])[:k]
            song_ids = [index.song_ids[i[0]] for i in top_k]
            scores = [i[1] for i in top_k]

        # get songs
        songs = Song.objects.filter(song_id__in=song_ids)
        response: dict = {
            "Songs": SongSerializer(songs, many=True, context={'request': request}).data,
            "Scores": scores
        }
        return response




    @catch_exceptions
    def list(self, request, *args, **kwargs):
        # Will recreate the search index for all songs
        response: dict = {}

        # collect artist, title, album, genre, description from the songs and put them in a single string to be used
        # for tf-idf
        songs = Song.objects.all()
        new_index = Index()

        for song in songs:
            # remove all non-alphanumeric characters
            artist = song.artist.replace(",", "").replace("(", "").replace(")", "").lower()
            title = song.title.replace(",", "").replace("(", "").replace(")", "").lower()
            album = song.album.replace(",", "").replace("(", "").replace(")", "").lower()
            genre = song.genre.replace(",", "").replace("(", "").replace(")", "").lower()
            description = song.description.replace(",", "").replace("(", "").replace(")", "").lower()

            doc = artist + " " + title + " " + album + " " + genre + " " + description + " " + song.camelot_key
            if song.popularity > 60:
                doc += " " + "popular"
            if song.energy > 75 and song.danceability > 75:
                doc += " " + "danceable" + " " + "hype"
            elif song.energy > 75 and song.speechiness > 20:
                doc += " " + "hype"

            new_index.concatenations.append(doc)
            new_index.tokenized_concatenations.append(
                doc.split()
            )

            new_index.song_ids.append(song.song_id)

        # Index for TF-IDF
        new_index.tfidf_matrix = new_index.vectorizer.fit_transform(new_index.concatenations)

        # Index for SVD
        new_index.dictionary = corpora.Dictionary(new_index.tokenized_concatenations)
        corpus = [new_index.dictionary.doc2bow(text) for text in new_index.tokenized_concatenations]
        new_index.lsi_model = models.LsiModel(corpus, id2word=new_index.dictionary, num_topics=len(songs))
        new_index.lsi_index = similarities.MatrixSimilarity(new_index.lsi_model[corpus])


        # save index
        joblib.dump(new_index, settings.INDEX_PATH)

        return response
