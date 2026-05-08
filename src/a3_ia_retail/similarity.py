import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def product_similarity_recommendations(
    basket: pd.DataFrame,
    top_n: int = 5,
    min_similarity: float = 0.05,
) -> pd.DataFrame:
    """Rank related products by cosine similarity of invoice presence."""
    product_invoice = basket.T.astype(int)
    matrix = cosine_similarity(product_invoice)
    similarity_df = pd.DataFrame(matrix, index=product_invoice.index, columns=product_invoice.index)
    rows = []

    for product in similarity_df.index:
        related = similarity_df.loc[product].drop(index=product).sort_values(ascending=False).head(top_n)
        for recommended_product, score in related.items():
            if score >= min_similarity:
                rows.append(
                    {
                        "product": product,
                        "recommended_product": recommended_product,
                        "similarity": score,
                    }
                )

    if not rows:
        return pd.DataFrame(columns=["product", "recommended_product", "similarity"])

    return pd.DataFrame(rows).sort_values(["product", "similarity"], ascending=[True, False])
