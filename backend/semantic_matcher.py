from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(jd_text, resume_text):
    # Use TF-IDF which is much lighter on memory than PyTorch
    vectorizer = TfidfVectorizer(stop_words='english')
    
    try:
        # Fit and transform both texts to get their TF-IDF vectors
        tfidf_matrix = vectorizer.fit_transform([jd_text, resume_text])
        
        # Compute cosine similarity between the two vectors
        score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return score
    except Exception:
        return 0.0