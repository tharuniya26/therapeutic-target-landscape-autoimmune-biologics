from pathlib import Path
from src.data_validation import validate_all, validate_uniprot_id


def test_canonical_uniprot_accessions():
    assert validate_uniprot_id("P01375")
    assert validate_uniprot_id("Q96RJ3")
    assert not validate_uniprot_id("TNF")


def test_research_tables_validate():
    result = validate_all(Path("data/processed"))
    assert result == {name: [] for name in result}

