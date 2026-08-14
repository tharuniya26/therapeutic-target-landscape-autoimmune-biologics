from src.target_mapping import association_matrix, direct_edges


def test_direct_edge_creation(evidence):
    assert direct_edges(evidence) == [("Drug A", "TNF")]


def test_matrix_means_documented_evidence(evidence):
    matrix = association_matrix(evidence)
    assert matrix.loc["Drug A", "TNF"] == 1

