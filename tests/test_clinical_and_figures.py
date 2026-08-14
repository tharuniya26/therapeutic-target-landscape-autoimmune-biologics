import pandas as pd
from src.clinical_evidence import evidence_summary
from src.drug_catalog import approved_records
from src.network_analysis import build_network
from src.pathway_analysis import target_pathway_matrix
from src.visualization import generate_figures


def test_missing_trial_identifier_is_retained_not_invented():
    frame = pd.DataFrame([{"disease":"PsA","phase":"2","trial_identifier":""}])
    assert evidence_summary(frame).iloc[0].study_count == 1
    assert frame.iloc[0].trial_identifier == ""


def test_designation_is_not_approval():
    frame = pd.DataFrame({"regulatory_status":["approved","breakthrough therapy designation; not recorded as approved"],"jurisdiction":["US","US"]})
    assert len(approved_records(frame)) == 1


def test_all_registered_figures_generate(tmp_path):
    catalog = pd.read_csv("data/processed/biologic_drug_catalog.csv")
    evidence = pd.read_csv("data/processed/drug_target_evidence.csv")
    targets = pd.read_csv("data/processed/therapeutic_targets.csv")
    clinical = pd.read_csv("data/processed/clinical_evidence.csv")
    paths = generate_figures(catalog, evidence, clinical, build_network(catalog, evidence), target_pathway_matrix(targets), tmp_path)
    assert len(paths) == 10
    assert all(path.stat().st_size > 0 for path in paths)

