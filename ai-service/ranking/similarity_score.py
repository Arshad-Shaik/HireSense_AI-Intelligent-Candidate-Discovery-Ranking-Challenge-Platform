# ai-service/ranking/similarity_score.py

def compute_similarity_score(distance):
    """
    Convert Chroma distance into a bounded similarity score.
    """

    similarity = 1.0 / (1.0 + distance)

    return round(similarity, 4)