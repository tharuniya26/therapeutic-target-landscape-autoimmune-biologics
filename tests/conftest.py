import pandas as pd
import pytest


@pytest.fixture
def evidence():
    return pd.DataFrame([
        {"drug_name":"Drug A","target_gene":"TNF","target_uniprot_id":"P01375","interaction_mechanism":"neutralization","relationship":"direct","evidence_source":"source","verification_status":"verified"}
    ])


@pytest.fixture
def catalog():
    return pd.DataFrame([
        {"drug_name":"Drug A","autoimmune_indication":"Disease A","regulatory_status":"approved","jurisdiction":"Testland"}
    ])

