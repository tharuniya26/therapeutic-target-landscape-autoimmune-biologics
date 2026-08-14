"""Descriptive pathway mapping for a non-random curated target panel."""

from __future__ import annotations
from pathlib import Path
import pandas as pd

PATHWAYS: dict[str, tuple[str, ...]] = {
    "TNF signaling / NF-kB": ("TNF",),
    "B-cell depletion": ("MS4A1",),
    "IL-6 signaling": ("IL6R",),
    "B-cell survival": ("TNFRSF13C", "TNFSF13B", "TNFSF13"),
    "IL-17 signaling": ("IL17A", "IL17F"),
    "IgG homeostasis": ("FCGRT",),
    "Terminal complement": ("C5",),
    "CD40 co-stimulation": ("CD40LG",),
}


def target_pathway_matrix(targets: pd.DataFrame) -> pd.DataFrame:
    """Map membership only; membership does not imply inhibition direction."""
    genes = targets["target_gene"].tolist()
    return pd.DataFrame({p: [int(g in members) for g in genes] for p, members in PATHWAYS.items()}, index=genes)


def export_matrix(targets_path: str | Path, output: str | Path) -> pd.DataFrame:
    matrix = target_pathway_matrix(pd.read_csv(targets_path))
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    matrix.rename_axis("target_gene").to_csv(output)
    return matrix

