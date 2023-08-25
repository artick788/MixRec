class Index:
    def __init__(self):
        self.concatenations: [str] = []
        self.tokenized_concatenations: [[str]] = []
        self.song_ids = []
        # for TF.IDF calculation
        self.vectorizer = None
        self.tfidf_matrix = None
        # for LSI calculation
        self.dictionary = None      # for mapping between words and their integer ids
        self.lsi_model = None       # for LSI calculation
        self.lsi_index = None