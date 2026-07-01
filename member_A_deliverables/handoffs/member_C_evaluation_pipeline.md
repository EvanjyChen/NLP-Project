# David Kim (C) Handoff: Evaluation Pipeline

## Objective

Implement a reproducible evaluation harness for identity and Sankeerth Adisha's
systems, covering CEFR target control, source/reference meaning preservation,
supplementary metrics, and uncertainty. David Kim (C) does not provide a runtime
service to Sankeerth and independently recomputes all final evaluation scores.

## Inputs

Read:

- `member_A_deliverables/data/processed/tsar2025_normalized.jsonl`
- `member_A_deliverables/data/processed/identity_baseline.jsonl`
- `member_A_deliverables/docs/data_schema.md`
- `member_A_deliverables/docs/split_policy.md`
- Frozen predictions under `member_B_deliverables/predictions/`

Official public evaluator resources are listed in
`member_A_deliverables/docs/data_source.md`.

## Dependency Contract with Sankeerth Adisha

David does not need to wait for Sankeerth to implement the evaluator:

1. David builds prediction validation, CEFR evaluation, semantic metrics,
   aggregation, caching, and tests using identity and synthetic predictions.
2. Sankeerth independently builds generation and self-refinement with a local CEFR
   critic. David provides no feedback API or runtime service.
3. After Sankeerth freezes all predictions, David receives only:
   - `member_B_deliverables/predictions/*.jsonl`;
   - `member_B_deliverables/manifests/*.json`;
   - `member_B_deliverables/critic/manifest.json`;
   - the SHA-256 hashes for those files.
4. David validates the hashes, treats the prediction files as immutable, and
   independently recomputes all final scores from output text.
5. Sankeerth's critic outputs may be analyzed as generation metadata but must not be
   copied into David's final metric tables.

Therefore, David's implementation has no dependency on Sankeerth. Only David's final
full-system evaluation depends on Sankeerth's frozen prediction bundle.

## Required Output Directory

Create:

```text
member_C_deliverables/
  README.md
  configs/
  scripts/
  tests/
  cache/
  results/
    per_instance/
    aggregate/
    main_results.csv
    main_results.md
  manifests/
```

Do not modify Member A or Sankeerth Adisha (B) prediction files.

## Implementation Tasks

### C-01: Prediction Validation and Alignment

- Parse JSONL structurally.
- Require exactly one prediction for every expected ID.
- Reject duplicate, missing, extra, empty, or split/target-mismatched rows.
- Join by `id`, never by row position.
- Preserve the original prediction file and record its SHA-256 hash.

### C-02: CEFR Evaluation

- Use the three organizer-published ModernBERT checkpoints listed in
  `member_A_deliverables/docs/data_source.md`.
- Read the model cards and shared-task paper before implementing ensemble behavior.
- Reproduce the documented confidence-based ensemble; do not assume majority voting
  without verification.
- Cache per-checkpoint class probabilities for every output.
- Report at minimum:
  - exact target accuracy;
  - adjusted/adjacent accuracy if the official definition is confirmed;
  - CEFR RMSE using an explicitly documented ordinal mapping;
  - weighted F1 where applicable.
- Report all target-control metrics separately for A2 and B1.

### Independence Boundary

- Do not implement a feedback API or blocking service for Sankeerth Adisha (B).
- Develop the entire harness using identity and synthetic prediction fixtures before
  Sankeerth finishes.
- When Sankeerth's predictions arrive, recompute CEFR and semantic scores from final output
  text.
- Ignore Sankeerth's generation-time critic predictions when calculating final
  metrics.
- Record both Sankeerth's critic configuration and David's evaluator configuration so
  the paper can distinguish generation control from independent evaluation.

### C-03: Meaning Preservation

- Implement MeaningBERT source-to-output and reference-to-output scoring according to
  the shared-task evaluation description.
- Pin model/package revisions.
- Cache embeddings or per-instance scores so repeated aggregation does not rerun
  neural inference.
- If the authoritative implementation cannot be located, label the result as a
  reproduction and document the exact package/checkpoint used.
- Add BERTScore only as a supplementary measure.

### C-04: Optional Simplification Metrics

- Add SARI or LENS only after confirming paragraph-level input support.
- Do not treat BLEU as a primary metric.
- Keep the heuristic FKGL from Member A separate from CEFR predictions.
- Clearly label every metric as official, reproduced, or supplementary.

### C-05: Aggregation and Uncertainty

Produce per-instance rows containing:

- ID, system, target, predicted CEFR, confidence;
- exact-match indicator and ordinal error;
- MeaningBERT source and reference scores;
- revision count and any supplementary scores.

Produce aggregate rows by system and by A2/B1. Add paired bootstrap confidence
intervals or paired randomization tests for planned system comparisons. Fix and record
the resampling seed.

### C-06: Sanity Checks

- Run the identity baseline first.
- Verify identity has perfect source similarity but poor simplification control.
- Evaluate human references as an oracle/sanity condition where permitted.
- Manually inspect at least five per-instance joins and score directions.

## Main Results Contract

`main_results.csv` and `.md` should contain:

| System | Target | N | CEFR exact acc. | CEFR RMSE | MB-source | MB-reference | Mean revisions |
|---|---|---:|---:|---:|---:|---:|---:|

Include `ALL`, `A2`, and `B1` rows for every system.

## Minimum Tests

- Duplicate, missing, extra, and target-mismatched predictions are rejected.
- Joining is invariant to prediction row order.
- CEFR ordinal mapping and RMSE are correct on a hand-calculated fixture.
- Exact and adjacent accuracy are correct on a fixture.
- Aggregation separates A2 and B1 correctly.
- Sankeerth's generation-time critic fields do not affect final metric calculations.
- Cached and uncached evaluator paths return the same scores.
- Bootstrap results are deterministic for a fixed seed.

Neural model calls should be mocked in unit tests. Add one opt-in integration smoke
test for downloaded checkpoints.

## Definition of Done

- Identity plus all frozen Sankeerth Adisha (B) prediction files pass alignment validation.
- Official/reproduced CEFR and MeaningBERT scores are available per instance.
- Main tables contain ALL/A2/B1 rows and metric directions are documented.
- Final scores are independently recomputed rather than copied from Sankeerth's
  critic logs.
- Model revisions, prediction hashes, environment, and seeds are recorded.
- Unit tests pass; neural smoke-test status is documented.

## LLM Implementation Prompt

Use the following as the initial instruction for a coding LLM:

```text
You are David Kim (C) for an NLP research project. Implement the evaluation pipeline
described in
member_A_deliverables/handoffs/member_C_evaluation_pipeline.md.

First read Member A's data source, schema, and split policy documents. Create all work
under member_C_deliverables/ and never alter Member A data or Sankeerth Adisha (B) predictions.
Implement prediction alignment and metric aggregation test-first, using fake CEFR and
similarity scorers so unit tests need no network or GPU. Then integrate the three
organizer-published ModernBERT checkpoints and the best authoritative MeaningBERT
implementation you can verify. Clearly distinguish official, reproduced, and
supplementary metrics. Do not build a runtime feedback service for Sankeerth and do
not reuse Sankeerth's generation-time critic scores. Cache neural outputs, pin revisions, and
produce per-instance and aggregate ALL/A2/B1 results. Complete the harness with
identity and synthetic fixtures before Sankeerth finishes, then evaluate Sankeerth's
frozen files.
Run identity baseline sanity checks first.

Report files changed, checks run, model downloads performed, and any uncertainty about
the official ensemble or MeaningBERT implementation.
```
