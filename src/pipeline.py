"""Single-command build for validation, analyses, figures, notebooks, and report."""

from __future__ import annotations
import json
from pathlib import Path
import nbformat as nbf
import pandas as pd
from .data_validation import validate_all
from .network_analysis import build_network, export_network
from .pathway_analysis import export_matrix
from .visualization import generate_figures


ROOT = Path(__file__).resolve().parents[1]


def create_notebooks() -> None:
    specs = [
        ("01_data_collection", "Curated data collection", "Load the indication-specific catalog and audit source fields.", "catalog[['drug_name','autoimmune_indication','regulatory_status','jurisdiction']].head(13)"),
        ("02_drug_target_mapping", "Drug–target mapping", "Construct an observed direct-evidence matrix.", "association_matrix(evidence)"),
        ("03_therapeutic_network", "Therapeutic network", "Build and summarize the typed heterogeneous graph.", "network_metrics(graph).groupby('node_type').agg(nodes=('node','count'), mean_degree=('degree','mean'))"),
        ("04_pathway_analysis", "Pathway mapping", "Describe target membership without inappropriate enrichment testing.", "target_pathway_matrix(targets)"),
        ("05_clinical_evidence_analysis", "Clinical evidence", "Summarize coverage without cross-trial efficacy ranking.", "evidence_summary(clinical)"),
        ("06_biologic_modality_analysis", "Modality analysis", "Compare curated architectures without inferring superiority.", "modality_counts(ROOT/'data/processed/biologic_drug_catalog.csv')"),
        ("07_integrated_results", "Integrated results", "Report reproducible counts and link to generated outputs.", "{'drugs': catalog.drug_name.nunique(), 'targets': targets.target_gene.nunique(), 'direct_interactions': len(evidence), 'studies': len(clinical), 'graph_nodes': graph.number_of_nodes(), 'graph_edges': graph.number_of_edges()}"),
    ]
    setup = """from pathlib import Path\nimport sys\nROOT = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\nsys.path.insert(0, str(ROOT))\nimport pandas as pd\nfrom src.target_mapping import association_matrix\nfrom src.network_analysis import build_network, network_metrics\nfrom src.pathway_analysis import target_pathway_matrix\nfrom src.clinical_evidence import evidence_summary\nfrom src.modality_analysis import modality_counts\ncatalog=pd.read_csv(ROOT/'data/processed/biologic_drug_catalog.csv')\nevidence=pd.read_csv(ROOT/'data/processed/drug_target_evidence.csv')\ntargets=pd.read_csv(ROOT/'data/processed/therapeutic_targets.csv')\nclinical=pd.read_csv(ROOT/'data/processed/clinical_evidence.csv')\ngraph=build_network(catalog,evidence)"""
    for stem, title, rationale, expression in specs:
        nb = nbf.v4.new_notebook()
        nb["metadata"]["kernelspec"]={"display_name":"Python 3","language":"python","name":"python3"}
        nb.cells=[nbf.v4.new_markdown_cell(f"# {title}\n\n**Objective.** {rationale}\n\n**Sources.** Curated FDA/UniProt/ClinicalTrials.gov and peer-reviewed records documented in `docs/data_provenance.md`.\n\n**Limitations.** This is a deliberately scoped evidence map, not a systematic review or comparative efficacy analysis."), nbf.v4.new_code_cell(setup), nbf.v4.new_code_cell(expression), nbf.v4.new_markdown_cell("## Interpretation\n\nOutputs describe the curated graph and evidence coverage. Absence in the dataset is not evidence of biological absence. See the project limitations for selection and knowledge-base biases.")]
        path=ROOT/"notebooks"/f"{stem}.ipynb";path.parent.mkdir(parents=True,exist_ok=True);nbf.write(nb,path)


def run() -> dict[str, int]:
    errors=validate_all(ROOT/"data/processed")
    if any(errors.values()): raise ValueError(json.dumps(errors,indent=2))
    catalog=pd.read_csv(ROOT/"data/processed/biologic_drug_catalog.csv")
    evidence=pd.read_csv(ROOT/"data/processed/drug_target_evidence.csv")
    targets=pd.read_csv(ROOT/"data/processed/therapeutic_targets.csv")
    clinical=pd.read_csv(ROOT/"data/processed/clinical_evidence.csv")
    graph=build_network(catalog,evidence)
    export_network(graph,ROOT/"results/therapeutic_network.graphml",ROOT/"results/network_metrics.csv")
    matrix=export_matrix(ROOT/"data/processed/therapeutic_targets.csv",ROOT/"results/target_pathway_matrix.csv")
    figures=generate_figures(catalog,evidence,clinical,graph,matrix,ROOT/"figures")
    create_notebooks()
    summary={"drugs":catalog.drug_name.nunique(),"targets":targets.target_gene.nunique(),"interactions":len(evidence),"studies":len(clinical),"nodes":graph.number_of_nodes(),"edges":graph.number_of_edges(),"figures":len(figures)}
    (ROOT/"results/summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    return summary


if __name__ == "__main__": print(json.dumps(run(),indent=2))

