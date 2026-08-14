"""Schema and integrity checks for curated evidence tables."""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

UNIPROT_RE = re.compile(r"^(?:[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9](?:[A-Z][A-Z0-9]{2}[0-9]){1,2})$")

REQUIRED = {
    "biologic_drug_catalog.csv": {"drug_name", "target_gene", "autoimmune_indication", "regulatory_status", "jurisdiction", "verification_status"},
    "therapeutic_targets.csv": {"target_gene", "target_uniprot_id", "hgnc_id", "verification_status"},
    "drug_target_evidence.csv": {"drug_name", "target_gene", "relationship", "evidence_source", "verification_status"},
    "clinical_evidence.csv": {"trial_identifier", "investigated_drug", "disease", "phase", "main_reported_result", "verification_status"},
}


def validate_uniprot_id(value: str) -> bool:
    """Validate one canonical UniProt accession."""
    return bool(UNIPROT_RE.fullmatch(str(value)))


def validate_table(path: str | Path) -> list[str]:
    """Return human-readable validation errors for one CSV."""
    path = Path(path)
    frame = pd.read_csv(path).fillna("")
    errors: list[str] = []
    missing = REQUIRED.get(path.name, set()) - set(frame.columns)
    if missing:
        errors.append(f"missing columns: {sorted(missing)}")
    if frame.duplicated().any():
        errors.append("duplicate rows present")
    if "verification_status" in frame and not set(frame["verification_status"]).issubset({"verified", "not verified"}):
        errors.append("invalid verification status")
    if path.name == "therapeutic_targets.csv":
        invalid = frame.loc[~frame["target_uniprot_id"].map(validate_uniprot_id), "target_uniprot_id"].tolist()
        if invalid:
            errors.append(f"invalid UniProt accessions: {invalid}")
    return errors


def validate_all(data_dir: str | Path = "data/processed") -> dict[str, list[str]]:
    """Validate all four source tables."""
    root = Path(data_dir)
    return {name: validate_table(root / name) for name in REQUIRED}

