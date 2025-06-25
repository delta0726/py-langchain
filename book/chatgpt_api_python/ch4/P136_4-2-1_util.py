from scipy import spatial
from typing import List, Optional


def distances_from_embeddings(
    query_embedding: List[float],
    embeddings: List[List[float]],
    distance_metric="cosine",
) -> List[List]:
    """Return the distances between a query embedding and a list of embeddings."""
    distance_metrics = {
        "cosine": spatial.distance.cosine,
        "L1": spatial.distance.cityblock,
        "L2": spatial.distance.euclidean,
        "Linf": spatial.distance.chebyshev,
    }
    distances = [
        distance_metrics[distance_metric](query_embedding, embedding)
        for embedding in embeddings
    ]
    return distances


if __name__ == "__main__":
    query = [1.0, 0.0, 0.0]
    candidates = [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.5, 0.5, 0.0],
        [1.0, 1.0, 1.0],
    ]

    for metric in ["cosine", "L1", "L2", "Linf"]:
        print(f"--- {metric} ---")
        dists = distances_from_embeddings(query, candidates, distance_metric=metric)
        for i, dist in enumerate(dists):
            print(f"Embedding {i}: Distance = {dist:.4f}")
