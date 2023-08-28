from rest_framework.viewsets import ModelViewSet
from django.conf import settings

from .Decorators import catch_exceptions
from .Serializer import SongSerializer
from .models import Song
from .Index import Index
from .TermAssociations import get_assocations

from sklearn.feature_extraction.text import TfidfVectorizer
from gensim import corpora, models, similarities

from nltk.stem import PorterStemmer

import joblib


class IndexEP(ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    @catch_exceptions
    def create(self, request, *args, **kwargs):
        norm = request.data.get("norm", "l2")
        if norm == "None":
            norm = None
        use_idf = bool(request.data.get("use_idf", "True"))
        smooth_idf = bool(request.data.get("smooth_idf", "True"))
        sublinear_tf = bool(request.data.get("sublinear_tf", "False"))
        max_df = float(request.data.get("max_df", 1.0))
        min_df = int(request.data.get("min_df", 1))


        # collect artist, title, album, genre, description from the songs and put them in a single string to be used
        # for tf-idf
        songs = Song.objects.all()
        new_index = Index()
        new_index.vectorizer = TfidfVectorizer(analyzer='word',
                                               stop_words='english',
                                               lowercase=True,
                                               norm=norm,
                                               use_idf=use_idf,
                                               smooth_idf=smooth_idf,
                                               sublinear_tf=sublinear_tf,
                                               max_df=max_df,
                                               min_df=min_df
                                               )


        for song in songs:
            # remove all non-alphanumeric characters
            artist = song.artist.replace(",", "").replace("(", "").replace(")", "").lower()
            title = song.title.replace(",", "").replace("(", "").replace(")", "").lower()
            album = song.album.replace(",", "").replace("(", "").replace(")", "").lower()
            genre = song.genre.replace(",", "").replace("(", "").replace(")", "").lower()
            description = song.description.replace(",", "").replace("(", "").replace(")", "").lower()

            # stem description
            ps = PorterStemmer()
            description = " ".join([ps.stem(word) for word in description.split()])

            doc = artist + " " + title + " " + album + " " + genre + " " + description + " " + song.camelot_key
            associations = get_assocations(song)
            for association in associations:
                doc += " " + association

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

        return {}
