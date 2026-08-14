"""Convenience queries over indication-specific therapeutic records."""

from pathlib import Path
import pandas as pd


def load_catalog(path: str | Path = "data/processed/biologic_drug_catalog.csv") -> pd.DataFrame:
    """Load the curated catalog without collapsing drug-indication records."""
    return pd.read_csv(path).fillna("")


def approved_records(frame: pd.DataFrame, jurisdiction: str | None = None) -> pd.DataFrame:
    """Filter explicit approvals; designation and investigation are not approval."""
    result = frame[frame["regulatory_status"].str.startswith("approved")]
    return result if jurisdiction is None else result[result["jurisdiction"] == jurisdiction]

