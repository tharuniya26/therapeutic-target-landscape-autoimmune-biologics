"""Drug-target evidence operations."""

from pathlib import Path
import pandas as pd


def load_target_evidence(path: str | Path = "data/processed/drug_target_evidence.csv") -> pd.DataFrame:
    return pd.read_csv(path).fillna("")


def association_matrix(evidence: pd.DataFrame) -> pd.DataFrame:
    """Create 1/0 observed-evidence matrix; zero means no curated evidence."""
    matrix = pd.crosstab(evidence["drug_name"], evidence["target_gene"])
    return matrix.reindex(sorted(matrix.index), axis=0).reindex(sorted(matrix.columns), axis=1)


def direct_edges(evidence: pd.DataFrame) -> list[tuple[str, str]]:
    verified = evidence[(evidence["relationship"] == "direct") & (evidence["verification_status"] == "verified")]
    return list(verified[["drug_name", "target_gene"]].itertuples(index=False, name=None))

