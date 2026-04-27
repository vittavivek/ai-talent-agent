from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import hashlib

# Lazy load model and cache
_model = None
_jd_cache = {}

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def get_jd_embedding(jd_text):
    # Cache JD embeddings by hash to avoid recomputation
    jd_hash = hashlib.md5(jd_text.encode()).hexdigest()
    if jd_hash not in _jd_cache:
        model = get_model()
        _jd_cache[jd_hash] = model.encode([jd_text])
    return _jd_cache[jd_hash]

def compute_similarity(jd_text, resume_text):
    model = get_model()
    jd_emb = get_jd_embedding(jd_text)
    res_emb = model.encode([resume_text])

    score = cosine_similarity(jd_emb, res_emb)[0][0]
    return score