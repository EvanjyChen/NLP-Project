# Shaohua Liu (D) Handoff: Preliminary Paper Integration

## Objective

After Sankeerth Adisha (B) and David Kim (C) complete their work, produce a template-compliant preliminary
research paper of no more than four main-text pages, excluding references and
appendices. The paper must include a contextualized review of 20-24 papers,
exploratory data analysis, working baselines, preliminary results, qualitative
analysis, limitations, and concrete next steps.

The paper must report only traceable data, model settings, and results. Never invent
missing experiments, metric values, citations, model revisions, or human ratings.

## Required Inputs

### Member A

Read:

- `Instruction.md`
- `proposal_draft.md`
- `preliminary_paper_plan.md`
- `member_A_deliverables/README.md`
- `member_A_deliverables/docs/data_source.md`
- `member_A_deliverables/docs/data_schema.md`
- `member_A_deliverables/docs/split_policy.md`
- `member_A_deliverables/docs/data_section_draft.md`
- `member_A_deliverables/docs/literature_notes_data_eval.md`
- `member_A_deliverables/artifacts/eda/dataset_statistics.csv`
- `member_A_deliverables/artifacts/eda/dataset_statistics.md`
- `member_A_deliverables/artifacts/eda/length_distribution.png`

### Sankeerth Adisha (B)

Expected under `member_B_deliverables/`:

- README and environment/reproduction instructions
- Frozen prompt files
- Model, generation-time critic, and run manifests
- Zero-shot, three-shot, and self-refinement predictions
- Smoke/full-run logs, including local critic decisions for each revision
- Test results and prediction hashes

### David Kim (C)

Expected under `member_C_deliverables/`:

- README and metric reproduction instructions
- Per-instance metric files
- Aggregate `ALL`, `A2`, and `B1` result tables
- Identity and reference-oracle sanity checks
- Confidence intervals or paired significance results
- Metric/model manifests and prediction hashes

## Preflight Gate

Before writing Results, verify:

- Every reported system has one frozen prediction per expected ID.
- David Kim (C) evaluated the exact hashes published by Sankeerth Adisha (B).
- Result tables contain identity, zero-shot, three-shot, and self-refinement rows.
- Results are separated into `ALL`, `A2`, and `B1`.
- Metric directions and definitions are documented.
- Model names, revisions, prompts, seeds, and refinement limits are available.
- Sankeerth's generation-time critic is distinguished from David's independent final
  evaluator.
- No test reference entered Sankeerth Adisha (B)'s generation pipeline.
- All 20-24 bibliography entries resolve to real papers.

If a required artifact is absent, create
`member_D_deliverables/checks/missing_inputs.md`, list the missing item and owner, and
continue only with sections that do not depend on it. Do not estimate missing values.

## Required Output Directory

Create:

```text
member_D_deliverables/
  README.md
  paper/
    preliminary.tex
    references.bib
    appendix.tex
    figures/
    tables/
  literature/
    literature_matrix.csv
    synthesis.md
  qualitative_analysis/
    sampling_manifest.json
    taxonomy.md
    coded_examples.csv
  human_evaluation/
    rubric.md
    sample_manifest.json
    ratings.csv
    agreement.md
  checks/
    input_audit.md
    claim_evidence.md
    page_budget.md
    missing_inputs.md
    submission_checklist.md
  build/
    preliminary.pdf
```

Do not modify Member A, Sankeerth, or David's deliverables. Copy only final
figures/tables needed by the paper and record their source paths.

## Paper Structure and Page Budget

Use the instructor-provided template. If the template is not present, stop before
creating a substitute and record it as a missing input.

| Section | Target space | Required content |
|---|---:|---|
| Abstract | 120-150 words | Task, systems, data, metrics, one real result |
| Introduction | 0.5 page | Motivation, gap, RQ1-RQ3, contributions |
| Related Work | 0.8-0.9 page | Thematic synthesis of 20-24 papers |
| Data and Method | 0.8-0.9 page | Release, leakage policy, models, prompts, refinement |
| Experiments and Results | 1.2-1.4 pages | EDA, main metrics, A2/B1 results, uncertainty |
| Analysis and Limitations | 0.4-0.5 page | Failure cases, trade-offs, validity limits |
| Conclusion | 0.2-0.3 page | Supported answers and next experiments |

Write the Abstract last. Keep references and permitted appendices outside the
four-page main-text limit.

## Implementation Tasks

### D-01: Audit Inputs

- Inventory all Member A, Sankeerth, and David files and hashes.
- Cross-check Sankeerth Adisha (B) prediction hashes against David Kim (C) manifests.
- Record model, prompt, metric, data, and seed versions.
- Identify missing or contradictory claims before drafting.
- Treat Member A's observed release counts as operational counts and mention the
  published-count discrepancy concisely.

### D-02: Build the Literature Matrix

Create one row per paper with:

- citation key and verified URL/DOI;
- venue and year;
- task and dataset;
- method;
- evaluation;
- main finding;
- limitation;
- relation to this project;
- assigned theme.

Use 20-24 verified papers total. Member A's six notes are starting material, not the
entire review. Organize synthesis under:

1. text simplification data and traditional systems;
2. controllable and CEFR-based simplification;
3. LLM prompting, reranking, and self-refinement;
4. automatic and human evaluation.

Do not write one isolated paragraph per paper. Compare approaches and close each theme
with the unresolved issue addressed by this study.

### D-03: Integrate Data and Method

- Use the exact pinned data revisions and counts from Member A.
- State that the release contains paragraph-level trial/test data, not a training
  split.
- Explain that Sankeerth Adisha (B) received reference-free test inputs.
- Report the exact model checkpoint, quantization, decoding, prompt conditions,
  demonstration rule, and maximum two revisions from Sankeerth Adisha (B)'s manifests.
- Describe Sankeerth's fixed generation-time CEFR critic and make clear that its scores
  trigger revisions but are not the final reported evaluation.
- Describe CEFR and meaning metrics exactly as implemented by David Kim (C).
- State that David independently recomputed final scores from Sankeerth's frozen
  outputs.
- Distinguish official, reproduced, and supplementary metrics.

### D-04: Produce Main Tables and Figure

Create one main result table containing:

- system/prompt condition;
- target or `ALL`;
- sample size;
- CEFR exact accuracy;
- CEFR RMSE;
- MeaningBERT source similarity;
- MeaningBERT reference similarity;
- mean revisions for self-refinement.

Include A2/B1 rows when space permits; otherwise use a compact second panel. Report
confidence intervals or paired-test results in text or table notes.

Use at most:

- one compact EDA table or the length-distribution figure;
- one main result table;
- one qualitative example.

Every table and figure must be generated from an existing artifact or a documented
script. Do not manually type metric values into LaTeX if a structured source can
generate the table.

### D-05: Qualitative Error Analysis

Use a fixed, reproducible sample across:

- A2 and B1;
- baseline failure and self-refinement success;
- self-refinement regression or persistent failure.

Code examples using:

- target too complex;
- over-simplified;
- essential content omitted;
- meaning altered or hallucinated;
- discourse/coreference failure;
- ungrammatical or disfluent;
- evaluator-generator disagreement.

Show one concise example in the main paper. Put the larger coded set in the appendix.
Do not select only favorable examples.

### D-06: Human Evaluation

If human ratings are available, report:

- sampling method and number of outputs;
- blinded system order;
- adequacy, fluency, and simplicity rubric;
- number of raters;
- agreement statistic and aggregation rule.

If ratings are not available, do not generate them with an LLM and call them human.
Describe human evaluation as future work or clearly label any LLM-based evaluation as
automatic.

### D-07: Claim-Evidence Audit

For every contribution and conclusion, record in `checks/claim_evidence.md`:

| Claim | Evidence file/table | Supported scope | Caveat |
|---|---|---|---|

Check that:

- "improves" corresponds to a real paired result;
- small differences are not called significant without evidence;
- A2/B1 differences use target-specific rows;
- metric limitations are stated;
- no preliminary result is presented as state of the art.

### D-08: Build and Submission Check

- Compile the paper from a clean state.
- Confirm no missing references, figures, or LaTeX warnings affecting content.
- Confirm four-page main-text limit in the required template.
- Check figure/table readability at normal PDF zoom.
- Verify author list and resolve the proposal's four-versus-five-member inconsistency.
- Complete `checks/submission_checklist.md`.

## Definition of Done

- Correct instructor template is used.
- Main text is no more than four pages.
- Related Work contextualizes 20-24 verified papers.
- EDA and baseline results are real and reproducible.
- Main results match David Kim (C)'s aggregate files.
- Sankeerth's model/prompt settings are fully traceable.
- A2/B1 and meaning/readability trade-offs are discussed.
- Qualitative sampling is reproducible.
- Human and automatic evaluation are labeled correctly.
- Every major claim has evidence.
- PDF builds successfully with no missing citations or assets.

## LLM Implementation Prompt

After Sankeerth Adisha (B) and David Kim (C) finish, give a coding/writing LLM this instruction:

```text
You are Shaohua Liu (D), responsible for producing the preliminary research paper. Read and
execute:
member_A_deliverables/handoffs/member_D_paper_integration.md

First audit all required Member A, Sankeerth, and David inputs. Do not start Results until you
confirm that David Kim (C) evaluated the exact frozen prediction hashes from Sankeerth Adisha (B). Use
the instructor-provided template and create all work under member_D_deliverables/.

Complete the literature matrix, thematic related-work synthesis, paper draft,
structured result tables, qualitative analysis, claim-evidence audit, and compiled
PDF. Use only traceable experiment values and verified citations. Never invent missing
metrics, model settings, references, or human ratings. If an input is missing, record
it in checks/missing_inputs.md, continue independent work, and clearly report the
blocker.

Run all available LaTeX/build/validation checks. Continue through implementation and
verification rather than returning only a plan. At the end, report files created,
paper page count, checks run, missing inputs, and remaining factual uncertainties.
```
