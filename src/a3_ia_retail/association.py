from time import perf_counter

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth


def generate_association_rules(
    basket: pd.DataFrame,
    method: str,
    min_support: float = 0.02,
    min_confidence: float = 0.2,
) -> tuple[pd.DataFrame, float]:
    """Generate association rules with Apriori or FP-Growth."""
    algorithms = {
        "apriori": apriori,
        "fpgrowth": fpgrowth,
    }
    if method not in algorithms:
        raise ValueError("method deve ser 'apriori' ou 'fpgrowth'")

    started_at = perf_counter()
    itemsets = algorithms[method](basket, min_support=min_support, use_colnames=True)
    if itemsets.empty:
        elapsed = perf_counter() - started_at
        return pd.DataFrame(), elapsed

    rules = association_rules(itemsets, metric="confidence", min_threshold=min_confidence)
    elapsed = perf_counter() - started_at
    rules = rules.sort_values(["lift", "confidence", "support"], ascending=False)
    return _stringify_itemsets(rules), elapsed


def _stringify_itemsets(rules: pd.DataFrame) -> pd.DataFrame:
    output = rules.copy()
    for column in ["antecedents", "consequents"]:
        output[column] = output[column].apply(lambda values: ", ".join(sorted(values)))
    return output
