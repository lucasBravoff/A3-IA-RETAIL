import pandas as pd


def clean_online_retail(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Clean Online Retail rows and return the cleaned data plus a removal summary."""
    start_rows = len(df)
    cleaned = df.copy()

    masks = {
        "cancelled_invoices": cleaned["InvoiceNo"].astype(str).str.startswith("C"),
        "non_positive_quantity": cleaned["Quantity"] <= 0,
        "non_positive_price": cleaned["UnitPrice"] <= 0,
        "missing_description": cleaned["Description"].isna(),
    }

    summary_rows = []
    for reason, mask in masks.items():
        summary_rows.append({"reason": reason, "rows": int(mask.sum())})

    invalid_mask = pd.concat(masks.values(), axis=1).any(axis=1)
    cleaned = cleaned.loc[~invalid_mask].copy()
    cleaned["Description"] = (
        cleaned["Description"].astype(str).str.upper().str.strip().str.replace(r"\s+", " ", regex=True)
    )
    cleaned["Revenue"] = cleaned["Quantity"] * cleaned["UnitPrice"]

    summary_rows.append({"reason": "total_removed", "rows": start_rows - len(cleaned)})
    summary_rows.append({"reason": "remaining_rows", "rows": len(cleaned)})

    return cleaned, pd.DataFrame(summary_rows)

