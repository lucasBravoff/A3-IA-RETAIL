from pathlib import Path

import pandas as pd

from a3_ia_retail.config import REQUIRED_COLUMNS


def load_online_retail(path: str | Path) -> pd.DataFrame:
    """Load the Online Retail dataset from CSV or Excel."""
    data_path = Path(path)
    if not data_path.exists():
        raise FileNotFoundError(f"Arquivo nao encontrado: {data_path}")

    suffix = data_path.suffix.lower()
    if suffix == ".csv":
        df = pd.read_csv(data_path, encoding="ISO-8859-1")
    elif suffix in {".xlsx", ".xls"}:
        df = pd.read_excel(data_path)
    else:
        raise ValueError("Formato nao suportado. Use CSV, XLSX ou XLS.")

    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Colunas obrigatorias ausentes: {sorted(missing)}")

    return df


def basic_profile(df: pd.DataFrame) -> pd.DataFrame:
    """Return a compact profile with rows, columns, nulls and duplicate count."""
    return pd.DataFrame(
        [
            {"metric": "rows", "value": len(df)},
            {"metric": "columns", "value": df.shape[1]},
            {"metric": "duplicate_rows", "value": int(df.duplicated().sum())},
            {"metric": "null_descriptions", "value": int(df["Description"].isna().sum())},
            {"metric": "null_customer_ids", "value": int(df["CustomerID"].isna().sum())},
            {
                "metric": "cancelled_invoices",
                "value": int(df["InvoiceNo"].astype(str).str.startswith("C").sum()),
            },
        ]
    )

