# Data dictionary

`biologic_drug_catalog.csv` uses one row per selected drug–indication context. `regulatory_status`, `jurisdiction` and `regulatory_verification_date` must be interpreted together; designation is not approval. Semicolon-delimited values indicate a multi-target agent within the same record.

`therapeutic_targets.csv` records approved gene symbols, recommended protein names, canonical UniProt accessions, HGNC identifiers and broad target classes.

`drug_target_evidence.csv` contains one direct relationship per row. `interaction_mechanism` preserves ligand neutralization, receptor blockade, decoy binding, cytolysis and other mechanistic distinctions. `relationship=direct` excludes downstream pathway consequences.

`clinical_evidence.csv` records one selected study per row. Sample size is the randomized/enrolled number reported in the cited principal source. `main_reported_result` is a controlled narrative field, not a harmonized effect estimate. Missing trial identifiers remain blank rather than inferred.

Across tables, `verified` means checked against the cited source; it does not mean evidence is unbiased, complete or current indefinitely.

