# Member A Deliverables

This directory is the complete Member A handoff package for the TSAR 2025
readability-controlled text simplification project.

## Contents

| Path | Purpose |
|---|---|
| `data/raw/` | Pinned official trial/test JSONL files and dataset cards |
| `data/processed/` | Normalized inputs, few-shot pool, references, and identity baseline |
| `scripts/data_pipeline.py` | Validation, normalization, EDA, and baseline generator |
| `tests/test_data_pipeline.py` | Data-contract and leakage tests |
| `artifacts/eda/` | Paper-ready statistics and length figure |
| `docs/data_source.md` | Provenance, hashes, release discrepancies, and license caveat |
| `docs/data_schema.md` | Raw, normalized, generation, and prediction schemas |
| `docs/split_policy.md` | Development/evaluation separation and leakage policy |
| `docs/data_section_draft.md` | Preliminary-paper Data section draft |
| `docs/literature_notes_data_eval.md` | Six source-backed literature notes |
| `docs/handoff.md` | General team handoff |
| `handoffs/member_B_prompting_pipeline.md` | Implementation brief for Sankeerth Adisha (B) |
| `handoffs/member_C_evaluation_pipeline.md` | Implementation brief for David Kim (C) |
| `handoffs/member_D_paper_integration.md` | Paper integration brief for Shaohua Liu (D) |
| `handoffs/group_chat_status_message.md` | Ready-to-send team status message |
| `member_A_data_plan.md` | Original Member A execution plan |

## Verified Counts

- Trial: 40 requests from 20 unique source paragraphs.
- Test: 200 requests from 100 unique source paragraphs.
- Total: 240 A2/B1 requests from 120 unique source paragraphs.

## Reproduce

Run from the repository root:

```bash
MPLCONFIGDIR=/tmp/matplotlib python3 member_A_deliverables/scripts/data_pipeline.py
MPLCONFIGDIR=/tmp/matplotlib python3 -m pytest -q member_A_deliverables/tests
```

The first command can be run from another directory because default paths are anchored
to this deliverables directory.

## Handoff Order

1. Sankeerth Adisha (B) and David Kim (C) start in parallel. Sankeerth builds
   generation with a local CEFR critic; David builds evaluation with identity and
   synthetic fixtures.
2. Sankeerth Adisha (B) freezes prediction files, critic metadata, and manifests.
3. David Kim (C) validates the frozen hashes, joins references, and independently
   recomputes final scores.
4. David Kim (C) publishes aggregate metrics and per-instance scores.
5. Member A supports stratified analysis by target, length, and compression.
