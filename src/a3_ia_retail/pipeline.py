import argparse
from pathlib import Path

from a3_ia_retail.association import generate_association_rules
from a3_ia_retail.basket import create_basket
from a3_ia_retail.clustering import kmeans_product_recommendations
from a3_ia_retail.comparison import compare_methods, summarize_rules
from a3_ia_retail.config import PROCESSED_DATA_DIR, TABLES_DIR
from a3_ia_retail.data_loading import basic_profile, load_online_retail
from a3_ia_retail.eda import build_eda_tables
from a3_ia_retail.preprocessing import clean_online_retail


def run_pipeline(
    input_path: str | Path,
    min_support: float = 0.02,
    min_confidence: float = 0.2,
    kmeans_clusters: int = 12,
    kmeans_components: int = 50,
) -> None:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    raw = load_online_retail(input_path)
    basic_profile(raw).to_csv(TABLES_DIR / "eda_summary.csv", index=False)

    cleaned, cleaning_summary = clean_online_retail(raw)
    cleaning_summary.to_csv(TABLES_DIR / "cleaning_summary.csv", index=False)
    cleaned.to_csv(PROCESSED_DATA_DIR / "online_retail_clean.csv", index=False)

    for name, table in build_eda_tables(cleaned).items():
        table.to_csv(TABLES_DIR / f"{name}.csv", index=False)

    basket = create_basket(cleaned)
    basket.astype(int).to_csv(PROCESSED_DATA_DIR / "basket.csv")

    apriori_rules, apriori_time = generate_association_rules(
        basket, "apriori", min_support=min_support, min_confidence=min_confidence
    )
    apriori_rules.to_csv(TABLES_DIR / "apriori_rules.csv", index=False)

    fpgrowth_rules, fpgrowth_time = generate_association_rules(
        basket, "fpgrowth", min_support=min_support, min_confidence=min_confidence
    )
    fpgrowth_rules.to_csv(TABLES_DIR / "fpgrowth_rules.csv", index=False)

    kmeans_clusters_df, kmeans_recommendations, kmeans_time = kmeans_product_recommendations(
        basket,
        n_clusters=kmeans_clusters,
        n_components=kmeans_components,
    )
    kmeans_clusters_df.to_csv(TABLES_DIR / "kmeans_product_clusters.csv", index=False)
    kmeans_recommendations.to_csv(TABLES_DIR / "kmeans_recommendations.csv", index=False)

    comparison = compare_methods(
        [
            summarize_rules("apriori", apriori_rules, apriori_time),
            summarize_rules("fpgrowth", fpgrowth_rules, fpgrowth_time),
            {
                "method": "kmeans",
                "elapsed_seconds": kmeans_time,
                "rules": len(kmeans_recommendations),
                "avg_lift": None,
                "avg_confidence": None,
                "avg_support": None,
                "avg_recommendation_score": kmeans_recommendations["recommendation_score"].mean()
                if not kmeans_recommendations.empty
                else 0.0,
            },
        ]
    )
    comparison.to_csv(TABLES_DIR / "method_comparison.csv", index=False)

    print(f"Pipeline concluida. Resultados salvos em: {TABLES_DIR}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Pipeline do projeto A3 IA Retail.")
    parser.add_argument("--input", required=True, help="Caminho para o CSV/XLSX da base Online Retail.")
    parser.add_argument("--min-support", type=float, default=0.02)
    parser.add_argument("--min-confidence", type=float, default=0.2)
    parser.add_argument("--kmeans-clusters", type=int, default=12)
    parser.add_argument("--kmeans-components", type=int, default=50)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    run_pipeline(
        args.input,
        min_support=args.min_support,
        min_confidence=args.min_confidence,
        kmeans_clusters=args.kmeans_clusters,
        kmeans_components=args.kmeans_components,
    )


if __name__ == "__main__":
    main()
