from time import perf_counter

import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler


def kmeans_product_recommendations(
    basket: pd.DataFrame,
    n_clusters: int = 12,
    n_components: int = 50,
    top_n: int = 5,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, float]:
    """Cluster products by purchase pattern and recommend products from the same cluster."""
    started_at = perf_counter()
    product_invoice = basket.T.astype(int)
    product_names = product_invoice.index.to_list()

    matrix = csr_matrix(product_invoice.to_numpy())
    embeddings = _build_product_embeddings(
        matrix,
        n_components=n_components,
        random_state=random_state,
    )

    cluster_count = min(n_clusters, len(product_names))
    model = KMeans(n_clusters=cluster_count, random_state=random_state, n_init="auto")
    labels = model.fit_predict(embeddings)

    clusters = pd.DataFrame(
        {
            "product": product_names,
            "cluster": labels,
            "distance_to_centroid": model.transform(embeddings).min(axis=1),
        }
    ).sort_values(["cluster", "distance_to_centroid", "product"])

    recommendations = _recommend_within_clusters(
        product_names=product_names,
        embeddings=embeddings,
        labels=labels,
        top_n=top_n,
    )

    elapsed = perf_counter() - started_at
    return clusters, recommendations, elapsed


def _build_product_embeddings(
    matrix: csr_matrix,
    n_components: int,
    random_state: int,
):
    max_components = min(matrix.shape[0] - 1, matrix.shape[1] - 1, n_components)
    if max_components < 2:
        embeddings = matrix.toarray()
    else:
        svd = TruncatedSVD(n_components=max_components, random_state=random_state)
        embeddings = svd.fit_transform(matrix)

    return StandardScaler().fit_transform(embeddings)


def _recommend_within_clusters(
    product_names: list[str],
    embeddings,
    labels,
    top_n: int,
) -> pd.DataFrame:
    rows = []
    product_index = pd.Index(product_names)

    for cluster in sorted(set(labels)):
        cluster_positions = [index for index, label in enumerate(labels) if label == cluster]
        if len(cluster_positions) < 2:
            continue

        cluster_embeddings = embeddings[cluster_positions]
        scores = cosine_similarity(cluster_embeddings)
        cluster_products = product_index[cluster_positions]

        for local_index, product in enumerate(cluster_products):
            related_scores = pd.Series(scores[local_index], index=cluster_products).drop(index=product)
            related_scores = related_scores.sort_values(ascending=False).head(top_n)
            for recommended_product, similarity in related_scores.items():
                rows.append(
                    {
                        "product": product,
                        "recommended_product": recommended_product,
                        "cluster": cluster,
                        "similarity": similarity,
                    }
                )

    if not rows:
        return pd.DataFrame(columns=["product", "recommended_product", "cluster", "similarity"])

    return pd.DataFrame(rows).sort_values(
        ["cluster", "product", "similarity"],
        ascending=[True, True, False],
    )
