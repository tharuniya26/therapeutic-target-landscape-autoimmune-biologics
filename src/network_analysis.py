"""Typed drug-target-disease-pathway graph construction and metrics."""

from __future__ import annotations
from pathlib import Path
import networkx as nx
import pandas as pd
from .pathway_analysis import PATHWAYS


def build_network(catalog: pd.DataFrame, evidence: pd.DataFrame) -> nx.Graph:
    graph = nx.Graph(name="Autoimmune biologics evidence network")
    for row in evidence.itertuples():
        graph.add_node(row.drug_name, node_type="drug")
        graph.add_node(row.target_gene, node_type="target", uniprot=row.target_uniprot_id)
        graph.add_edge(row.drug_name, row.target_gene, relation="directly_targets", mechanism=row.interaction_mechanism)
    for row in catalog.itertuples():
        graph.add_node(row.drug_name, node_type="drug")
        graph.add_node(row.autoimmune_indication, node_type="disease")
        relation = "approved_for" if str(row.regulatory_status).startswith("approved") else "investigated_for"
        graph.add_edge(row.drug_name, row.autoimmune_indication, relation=relation, jurisdiction=row.jurisdiction)
    for pathway, genes in PATHWAYS.items():
        graph.add_node(pathway, node_type="pathway")
        for gene in genes:
            if graph.has_node(gene):
                graph.add_edge(gene, pathway, relation="participates_in")
    return graph


def network_metrics(graph: nx.Graph) -> pd.DataFrame:
    component = {}
    for index, nodes in enumerate(nx.connected_components(graph), start=1):
        component.update({node: index for node in nodes})
    rows = [{"node": n, "node_type": d["node_type"], "degree": graph.degree(n), "component": component[n]}
            for n, d in graph.nodes(data=True)]
    return pd.DataFrame(rows).sort_values(["node_type", "degree", "node"], ascending=[True, False, True])


def export_network(graph: nx.Graph, graphml_path: str | Path, metrics_path: str | Path) -> None:
    Path(graphml_path).parent.mkdir(parents=True, exist_ok=True)
    nx.write_graphml(graph, graphml_path)
    network_metrics(graph).to_csv(metrics_path, index=False)

