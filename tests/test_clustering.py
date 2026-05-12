import pandas as pd

from a3_ia_retail.clustering import kmeans_product_recommendations


def test_kmeans_product_recommendations_returns_clusters_and_recommendations():
    basket = pd.DataFrame(
        {
            "A": [1, 1, 0, 0],
            "B": [1, 1, 0, 0],
            "C": [0, 0, 1, 1],
            "D": [0, 0, 1, 1],
        },
        index=["order_1", "order_2", "order_3", "order_4"],
    ).astype(bool)

    clusters, recommendations, elapsed = kmeans_product_recommendations(
        basket,
        n_clusters=2,
        n_components=2,
        top_n=1,
    )

    assert len(clusters) == 4
    assert set(clusters.columns) == {"product", "cluster", "distance_to_centroid"}
    assert set(recommendations.columns) == {
        "product",
        "recommended_product",
        "cluster",
        "recommendation_score",
    }
    assert not recommendations.empty
    assert elapsed >= 0
