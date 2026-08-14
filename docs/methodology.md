# Computational methodology

Four manually audited CSV tables are validated for schema, duplicates, canonical UniProt formatting and controlled verification states. NetworkX constructs an undirected heterogeneous evidence graph with node types `drug`, `target`, `disease` and `pathway`. Relations are `directly_targets`, `approved_for`, `investigated_for` and `participates_in`; approval is assigned only when the catalog status begins with `approved`.

Reported node degree and connected components describe this selected graph. They are not measures of efficacy, causal importance or clinical priority. Pathway analysis is a descriptive membership matrix because the target list is small, intentionally selected and non-random; an over-representation p-value would be misleading. Clinical analyses count coverage by disease and phase and never rank therapies using incompatible endpoints.

Run `python -m src.pipeline`, then `pytest`. Inputs are immutable during analysis; outputs are written to `results/`, `figures/` and `notebooks/`.

