import pandas as pd


def create_basket(df: pd.DataFrame, min_items_per_invoice: int = 2) -> pd.DataFrame:
    """Create an invoice x product basket matrix with binary values."""
    invoice_sizes = df.groupby("InvoiceNo")["Description"].nunique()
    valid_invoices = invoice_sizes[invoice_sizes >= min_items_per_invoice].index
    filtered = df[df["InvoiceNo"].isin(valid_invoices)]

    basket = (
        filtered.groupby(["InvoiceNo", "Description"])["Quantity"]
        .sum()
        .unstack(fill_value=0)
        .gt(0)
        .astype(bool)
    )
    return basket

