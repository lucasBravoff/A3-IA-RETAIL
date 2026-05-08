import pandas as pd

from a3_ia_retail.preprocessing import clean_online_retail


def test_clean_online_retail_removes_invalid_rows_and_standardizes_description():
    df = pd.DataFrame(
        {
            "InvoiceNo": ["1", "C2", "3", "4"],
            "StockCode": ["A", "B", "C", "D"],
            "Description": ["  product one ", "product two", None, "product four"],
            "Quantity": [2, 1, 1, -1],
            "InvoiceDate": ["2010-12-01"] * 4,
            "UnitPrice": [3.5, 2.0, 1.0, 1.0],
            "CustomerID": [10, 20, 30, 40],
            "Country": ["United Kingdom"] * 4,
        }
    )

    cleaned, summary = clean_online_retail(df)

    assert len(cleaned) == 1
    assert cleaned.iloc[0]["Description"] == "PRODUCT ONE"
    assert cleaned.iloc[0]["Revenue"] == 7.0
    assert summary.loc[summary["reason"] == "total_removed", "rows"].iloc[0] == 3

