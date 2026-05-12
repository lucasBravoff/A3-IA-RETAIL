import pandas as pd


def compare_methods(metrics: list[dict]) -> pd.DataFrame:
    """Create a comparison table across recommendation methods."""
    return pd.DataFrame(metrics).sort_values("method")


def summarize_rules(method: str, rules: pd.DataFrame, elapsed_seconds: float) -> dict:
    """Summarize association rule quality for Apriori and FP-Growth."""
    if rules.empty:
        return {
            "method": method,
            "elapsed_seconds": elapsed_seconds,
            "rules": 0,
            "avg_lift": 0.0,
            "avg_confidence": 0.0,
            "avg_support": 0.0,
            "avg_recommendation_score": None,
        }

    return {
        "method": method,
        "elapsed_seconds": elapsed_seconds,
        "rules": len(rules),
        "avg_lift": float(rules["lift"].mean()),
        "avg_confidence": float(rules["confidence"].mean()),
        "avg_support": float(rules["support"].mean()),
        "avg_recommendation_score": None,
    }
