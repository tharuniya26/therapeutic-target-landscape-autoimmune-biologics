"""Publication-style, data-derived figures with colourblind-friendly palettes."""

from __future__ import annotations
from pathlib import Path
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import seaborn as sns

COLORS = {"drug": "#0072B2", "target": "#D55E00", "disease": "#009E73", "pathway": "#CC79A7"}


def _save(fig: plt.Figure, stem: Path) -> None:
    stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(stem.with_suffix(".png"), dpi=320, bbox_inches="tight", facecolor="white")
    fig.savefig(stem.with_suffix(".svg"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


def _title(ax: plt.Axes, title: str, subtitle: str) -> None:
    ax.set_title(title, loc="left", weight="bold", fontsize=17, pad=24)
    ax.text(0, 1.01, subtitle, transform=ax.transAxes, fontsize=11, color="#555555")


def generate_figures(catalog: pd.DataFrame, evidence: pd.DataFrame, clinical: pd.DataFrame,
                     graph: nx.Graph, pathway_matrix: pd.DataFrame, output_dir: str | Path = "figures") -> list[Path]:
    """Generate the ten registered figures and return PNG paths."""
    sns.set_theme(style="whitegrid", context="talk", font_scale=1.0)
    out = Path(output_dir)

    # 1 workflow
    fig, ax = plt.subplots(figsize=(13, 2.8)); ax.axis("off")
    steps = ["Source literature", "Evidence verification", "Curated datasets", "Network + pathways", "Clinical interpretation"]
    xs = range(len(steps))
    for x, label in zip(xs, steps):
        ax.text(x, 0.5, label, ha="center", va="center", bbox=dict(boxstyle="round,pad=.6", fc="#E8F1F8", ec="#0072B2"), fontsize=10)
        if x < len(steps)-1: ax.annotate("", (x+.72, .5), (x+.30, .5), arrowprops=dict(arrowstyle="->", color="#555"))
    ax.set_xlim(-.5, 4.5); ax.set_ylim(0, 1); ax.set_title("Reproducible research workflow", weight="bold", loc="left", fontsize=17)
    _save(fig, out/"figure_01_research_workflow")

    # 2 mechanisms
    mechanisms = catalog["mechanism_of_action"].value_counts().sort_values()
    fig, ax = plt.subplots(figsize=(9, 5)); mechanisms.plot.barh(ax=ax, color="#0072B2")
    _title(ax, "Therapeutic mechanism classification", "Unique curated drug–indication records; categories preserve mechanistic distinctions")
    ax.set_xlabel("Number of agents"); ax.set_ylabel(""); _save(fig, out/"figure_02_mechanism_classification")

    # 3 bipartite
    bip = nx.Graph(); bip.add_edges_from(evidence[["drug_name", "target_gene"]].itertuples(index=False, name=None))
    left = sorted(evidence.drug_name.unique()); pos = {n:(0,i) for i,n in enumerate(left)}
    right=sorted(evidence.target_gene.unique()); pos.update({n:(1,i*(max(len(left)-1,1)/max(len(right)-1,1))) for i,n in enumerate(right)})
    fig, ax=plt.subplots(figsize=(11,8)); nx.draw_networkx_edges(bip,pos,ax=ax,alpha=.35); nx.draw_networkx_nodes(bip,pos,nodelist=left,node_color=COLORS["drug"],node_size=720,ax=ax); nx.draw_networkx_nodes(bip,pos,nodelist=right,node_color=COLORS["target"],node_size=720,ax=ax); nx.draw_networkx_labels(bip,pos,font_size=11,font_color="black",ax=ax); ax.axis("off"); ax.set_title("Verified drug–target bipartite network",weight="bold",loc="left",fontsize=17); _save(fig,out/"figure_03_drug_target_bipartite")

    # 4 matrix
    matrix=pd.crosstab(evidence.drug_name,evidence.target_gene).reindex(sorted(evidence.drug_name.unique())).reindex(sorted(evidence.target_gene.unique()),axis=1)
    fig,ax=plt.subplots(figsize=(12,7.5)); sns.heatmap(matrix,cmap=sns.color_palette(["#F2F2F2","#D55E00"],as_cmap=True),cbar=False,linewidths=.7,ax=ax)
    _title(ax,"Drug–target evidence matrix","Orange = documented direct interaction; grey = no interaction documented in this curated scope"); ax.set_xlabel("Target gene");ax.set_ylabel("Drug");ax.tick_params(labelsize=11);_save(fig,out/"figure_04_drug_target_heatmap")

    # 5 heterogeneous graph
    pos=nx.spring_layout(graph,seed=17,k=.82,iterations=180); fig,ax=plt.subplots(figsize=(13,9))
    nx.draw_networkx_edges(graph,pos,alpha=.24,width=1.1,ax=ax)
    for kind,color in COLORS.items():
        nodes=[n for n,d in graph.nodes(data=True) if d["node_type"]==kind]
        nx.draw_networkx_nodes(graph,pos,nodelist=nodes,node_color=color,node_size=620,label=kind,ax=ax)
    nx.draw_networkx_labels(graph,pos,font_size=8.5,ax=ax);ax.legend(frameon=False,ncol=4,fontsize=12,loc="upper center");ax.axis("off");ax.set_title("Drug–target–disease–pathway evidence network",weight="bold",loc="left",fontsize=17);fig.subplots_adjust(left=.02,right=.98,top=.90,bottom=.02);_save(fig,out/"figure_05_heterogeneous_network")

    # 6 pathways
    fig,ax=plt.subplots(figsize=(12,7)); sns.heatmap(pathway_matrix.T,cmap=sns.color_palette(["#F5F5F5","#009E73"],as_cmap=True),cbar=False,linewidths=.7,ax=ax)
    _title(ax,"Immune pathway membership map","Membership is descriptive and does not independently encode pharmacological direction");ax.set_xlabel("Direct therapeutic target");ax.set_ylabel("Pathway system");ax.tick_params(labelsize=11);_save(fig,out/"figure_06_pathway_map")

    # 7 modalities
    mods=catalog.groupby("modality").drug_name.nunique().sort_values()
    fig,ax=plt.subplots(figsize=(11,7));mods.plot.barh(ax=ax,color="#CC79A7");_title(ax,"Curated biologic modalities","Counts are unique agents, not comparative efficacy");ax.set_xlabel("Unique agents");ax.set_ylabel("");_save(fig,out/"figure_07_modality_comparison")

    # 8 trial phase
    phases=clinical.phase.astype(str).value_counts().sort_index()
    fig,ax=plt.subplots(figsize=(8,5.5));phases.plot.bar(ax=ax,color="#E69F00",rot=0);_title(ax,"Clinical evidence landscape","Curated pivotal and precision-medicine studies by stated phase");ax.set_xlabel("Trial phase");ax.set_ylabel("Studies");_save(fig,out/"figure_08_clinical_evidence")

    # 9 precision evidence
    precision=clinical[clinical.study_acronym.isin(["R4RA","STRAP"])].copy()
    fig,ax=plt.subplots(figsize=(12,3.2));ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis("off")
    for i,row in enumerate(precision.itertuples()):
        summary=textwrap.fill(f"{row.study_acronym} (n={row.sample_size})\n{row.main_reported_result}",43)
        ax.text(.25+i*.5,.46,summary,ha="center",va="center",linespacing=1.25,
                bbox=dict(boxstyle="round,pad=.9",fc="#F3E8F1",ec="#CC79A7",lw=1.8),fontsize=12)
    ax.set_title("Precision-therapy evidence map",weight="bold",loc="left",fontsize=17,pad=8)
    fig.subplots_adjust(left=.03,right=.97,top=.82,bottom=.08);_save(fig,out/"figure_09_precision_evidence")

    # 10 translational state
    states=catalog.assign(state=catalog.regulatory_status.map(lambda x:"Approved" if str(x).startswith("approved") else "Investigational" if "investigational" in str(x) or "designation" in str(x) else "Other")).groupby("state").drug_name.nunique()
    fig,ax=plt.subplots(figsize=(8,5.5));states.plot.bar(ax=ax,color=["#009E73" if x=="Approved" else "#E69F00" for x in states.index],rot=0);_title(ax,"Translational status of curated agents","Status is tied to the catalogued indication and jurisdiction, verified 18 October 2026");ax.set_ylabel("Unique agents");ax.set_xlabel("");_save(fig,out/"figure_10_translational_landscape")
    return sorted(out.glob("figure_*.png"))

