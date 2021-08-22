import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os

class Similarity:
    def __init__(self):
        path = os.path.dirname(__file__)
        self.transformer = SentenceTransformer(path+'/sentence-transformers_paraphrase-xlm-r-multilingual-v1')

    def calculate(self, x, y):
        query_vec = self.transformer.encode(x).reshape(1,-1)
        corpus_vec = self.transformer.encode(y).reshape(1,-1)
        self.sim_score = cosine_similarity(query_vec, corpus_vec)
        
        return self.sim_score

# sim = Similarity()