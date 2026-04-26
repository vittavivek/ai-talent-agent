from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

def compute_similarity(jd_text, resume_text):
    jd_emb = model.encode([jd_text])
    res_emb = model.encode([resume_text])

    score = cosine_similarity(jd_emb, res_emb)[0][0]
    return score