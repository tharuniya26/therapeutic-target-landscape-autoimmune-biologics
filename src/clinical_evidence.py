"""Clinical evidence summaries without cross-trial efficacy ranking."""

from pathlib import Path
import pandas as pd


def load_clinical_evidence(path: str | Path = "data/processed/clinical_evidence.csv") -> pd.DataFrame:
    return pd.read_csv(path).fillna("")


def evidence_summary(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.groupby(["disease", "phase"], dropna=False).size().rename("study_count").reset_index()

