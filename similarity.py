from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')


def compute_similarity_batch(resume_texts, jd_text):
    jd_embedding = model.encode([jd_text])
    resume_embeddings = model.encode(resume_texts)

    scores = cosine_similarity(resume_embeddings, jd_embedding)
    return scores