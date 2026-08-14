"""Count curated modalities without inferring structural superiority."""

from pathlib import Path
import pandas as pd


def modality_counts(path: str | Path = "data/processed/biologic_drug_catalog.csv") -> pd.DataFrame:
    frame = pd.read_csv(path)
    return frame.groupby("modality")["drug_name"].nunique().sort_values(ascending=False).rename("drug_count").reset_index()

