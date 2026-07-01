# Member A Handoff

## Reproduce the Data Artifacts

From the project root:

```bash
MPLCONFIGDIR=/tmp/matplotlib python3 member_A_deliverables/scripts/data_pipeline.py
```

Expected summary:

```json
{
  "test_requests": 200,
  "total_requests": 240,
  "trial_requests": 40,
  "unique_sources": 120
}
```

Run validation tests:

```bash
MPLCONFIGDIR=/tmp/matplotlib python3 -m pytest -q member_A_deliverables/tests
```

Runtime requirements are Python 3.10 or newer and Matplotlib. Tests require pytest.
Core validation and statistics use the Python standard library.

## Sankeerth Adisha (B)

- Read `member_A_deliverables/data/processed/generation_inputs.jsonl`.
- Use demonstrations only from
  `member_A_deliverables/data/processed/few_shot_pool.jsonl`.
- Record model revision, prompt version, demonstration IDs, decoding settings, seed,
  and revision count.
- Return predictions using the schema in
  `member_A_deliverables/docs/data_schema.md`.
- Follow `member_A_deliverables/handoffs/member_B_prompting_pipeline.md`.

## David Kim (C)

- Join predictions to
  `member_A_deliverables/data/processed/tsar2025_normalized.jsonl` by `id`.
- Start with `member_A_deliverables/data/processed/identity_baseline.jsonl`.
- Confirm every expected ID appears exactly once before running metrics.
- Treat the three CEFR checkpoints in the official Hugging Face collection as the
  authoritative public evaluator resources.
- Do not call the HULAT participant metric file an official organizer script.
- Follow `member_A_deliverables/handoffs/member_C_evaluation_pipeline.md`.

## Shaohua Liu (D)

- Use `member_A_deliverables/artifacts/eda/dataset_statistics.md` for the compact
  table.
- Use `member_A_deliverables/artifacts/eda/length_distribution.png` only if space
  permits.
- Integrate `member_A_deliverables/docs/data_section_draft.md` into the paper and
  verify its claims.
- Cite the shared-task paper and include the pinned release details.
- After Sankeerth Adisha (B) and David Kim (C) finish, follow
  `member_A_deliverables/handoffs/member_D_paper_integration.md`.

## Known Limitations

- Public release counts differ from the shared-task paper.
- Dataset cards do not declare a standalone dataset license.
- No source CEFR value is supplied per record.
- FKGL uses a deterministic local syllable heuristic and is descriptive only.
- Type-token ratio depends on paragraph length and should not be overinterpreted.
- Official neural metrics were not executed because they require model downloads and
  belong to David Kim (C)'s evaluation work.
