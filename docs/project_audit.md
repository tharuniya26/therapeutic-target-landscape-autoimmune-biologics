# Final project audit

Audit date: 19 October 2026. Status vocabulary: **PASSED**, **FAILED**, **NOT VERIFIED**.

## Final PDF layout and presentation

| Check | Status | Evidence |
|---|---|---|
| Final PDF rebuild | PASSED | `reports/build_report.py` completed two XeLaTeX passes and produced a 24-page PDF using Times New Roman. |
| All PDF pages visually inspected | PASSED | All 24 pages were rendered to images and reviewed for blank pages, isolated lines, cropping, overlap, margins, numbering, captions, tables, references, URLs, and section breaks. |
| Figure quality | PASSED | Ten figures were regenerated as 320-DPI PNG and SVG files. Embedded figures retain aspect ratio; labels, legends, axes, margins, and network-node text were visually checked. The precision-evidence map was redesigned with larger study boxes and text. |
| Figure captions | PASSED | Six report captions use consistent readable formatting, correct numbering, direct placement beneath the relevant figure, and explanatory scientific wording. Figures and captions are kept together in non-floating blocks. |
| Printed page 8 layout | PASSED | Figure 1, its caption, the following subsection heading, and explanatory paragraph share the page; the page is no longer figure-only. |
| Figure 2 wording | PASSED | The sentence was confirmed to belong to the pathway paragraph, not the caption. It now distinguishes cell-surface receptor blockade from soluble receptor-based ligand sequestration, using etanercept as the decoy example. |
| Printed page 15 layout | PASSED | The isolated-line problem is absent. The reproducibility paragraph remains intact and is followed naturally by the References section rather than an unnecessary page break. |
| Widow and orphan control | PASSED | LaTeX widow, club, and display-widow penalties are set to 10000; no isolated paragraph line was found during the page review. |
| Table layout | PASSED | All tables remain within margins. The appendix output table uses a smaller font and wider filename column so `therapeutic_network.graphml` does not cross into the purpose column. |
| References and citations | PASSED | Thirty numbered references render in citation order; no undefined citation or reference errors occur in the final LaTeX log. |
| Live re-verification of every citation and regulatory status after the 2026-10-18 snapshot | NOT VERIFIED | The final task audited rendering and repository integrity; statuses remain explicitly date- and jurisdiction-specific and require future scheduled rechecking. |

## Repository verification

| Area | Status | Evidence |
|---|---|---|
| Original source preserved and excluded from public version control | PASSED | The DOCX remains under `source_material_private/`, which is listed in `.gitignore`; public report materials contain no assignment cover, university logo, Turnitin image, registration number, or AI-declaration page. |
| Authorship | PASSED | Public report and README identify **Tharuniya Anpalakan** as author; the cover contains the requested department, university, location, and email and contains no date. |
| Curated drug catalog | PASSED | `biologic_drug_catalog.csv` contains 13 unique biologics with indication, jurisdiction, verification date, source, and status. |
| Therapeutic target dataset | PASSED | `therapeutic_targets.csv` contains 11 unique standardized human targets with HGNC symbols and canonical UniProt accessions. |
| Drug–target evidence | PASSED | `drug_target_evidence.csv` contains 16 verified direct relationships with explicit mechanisms and sources. |
| Clinical evidence | PASSED | `clinical_evidence.csv` contains 10 selected studies with design, endpoint, result, and limitation fields; the project does not perform cross-trial efficacy ranking. |
| Network and results | PASSED | GraphML, node metrics, target–pathway matrix, and summary outputs are present; the final network contains 39 nodes and 40 typed edges. |
| Scientific figures | PASSED | Ten PNG and ten SVG figures are present and reproducibly generated from the curated data. |
| Executable code | PASSED | Modular Python source, pipeline, pinned dependencies, and report builder are present. |
| Jupyter notebooks | PASSED | `python scripts/execute_notebooks.py` executed all seven notebooks on 19 October 2026; each reported two executed code cells and saved outputs. |
| Automated tests | PASSED | Final `python -m pytest` run on 19 October 2026: **10 passed, 0 failed**. |
| README and local links | PASSED | README reproducibility instructions are present; all eight local document and figure links resolve to existing files. |
| Build-artifact controls | PASSED | `.gitignore` excludes Python caches, LaTeX auxiliaries, temporary PDF renders, and private source material while retaining the LaTeX source and final PDF. |
| Git history/state | NOT VERIFIED | This workspace is not currently initialized as a Git repository, so commit history and remote configuration could not be audited. No push was attempted. |

## Remaining limitations

- The landscape is purposive rather than a systematic review; exhaustive coverage is **NOT VERIFIED**.
- Regulatory and clinical status is a dated snapshot and should be rechecked before a future public release.
- Formal dual-curator adjudication is **NOT VERIFIED**.
- The directory is content-ready for GitHub but still requires `git init` (or placement in an existing repository), review of the initial staged file list, and a user-authorized push.

## Release assessment

**READY FOR GITHUB** at the content and reproducibility level. The public file set, final PDF, report source, datasets, notebooks, figures, code, tests, citations, author presentation, and ignore rules passed the checks above. Git initialization and any remote push remain deliberate user actions.
