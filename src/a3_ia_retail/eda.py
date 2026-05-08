import pandas as pd


def build_eda_tables(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Build the first EDA tables requested in the project brief."""
    by_country = (
        df.groupby("Country", as_index=False)
        .agg(orders=("InvoiceNo", "nunique"), revenue=("Revenue", "sum"))
        .sort_values(["revenue", "orders"], ascending=False)
        .head(15)
    )

    top_quantity = (
        df.groupby(["StockCode", "Description"], as_index=False)
        .agg(quantity=("Quantity", "sum"), revenue=("Revenue", "sum"), orders=("InvoiceNo", "nunique"))
        .sort_values("quantity", ascending=False)
        .head(20)
    )

    top_revenue = top_quantity.sort_values("revenue", ascending=False).head(20)

    return {
        "country_summary": by_country,
        "top_products_by_quantity": top_quantity,
        "top_products_by_revenue": top_revenue,
    }

