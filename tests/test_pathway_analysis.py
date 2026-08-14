import pandas as pd
from src.pathway_analysis import target_pathway_matrix


def test_pathway_membership_is_binary():
    matrix = target_pathway_matrix(pd.DataFrame({"target_gene":["TNF","C5"]}))
    assert matrix.loc["TNF", "TNF signaling / NF-kB"] == 1
    assert matrix.loc["C5", "Terminal complement"] == 1
    assert set(matrix.to_numpy().ravel()) <= {0, 1}

