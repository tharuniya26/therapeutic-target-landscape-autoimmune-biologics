from src.network_analysis import build_network, network_metrics


def test_typed_network_and_regulatory_edge(catalog, evidence):
    graph = build_network(catalog, evidence)
    assert graph["Drug A"]["Disease A"]["relation"] == "approved_for"
    assert graph["Drug A"]["TNF"]["relation"] == "directly_targets"
    assert "component" in network_metrics(graph)


def test_investigational_not_approved(catalog, evidence):
    catalog.loc[0, "regulatory_status"] = "investigational"
    graph = build_network(catalog, evidence)
    assert graph["Drug A"]["Disease A"]["relation"] == "investigated_for"

