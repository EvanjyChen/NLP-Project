# Data Schema

## Raw Records

Both official JSONL files contain one object per generation request:

| Field | Type | Meaning |
|---|---|---|
| `dataset_id` | string | Release identifier, such as `tsar2025trial` |
| `text_id` | string | Request ID; suffix encodes target (`-a2` or `-b1`) |
| `original` | string | Source paragraph |
| `target_cefr` | string | Requested CEFR level |
| `reference` | string | One human reference simplification |

The validator requires every source ID to have exactly one A2 and one B1 request.

## Normalized Evaluation Records

`member_A_deliverables/data/processed/tsar2025_normalized.jsonl` is intended for
David Kim (C):

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Lowercase request ID |
| `source_id` | string | ID shared by the A2/B1 pair |
| `dataset_id` | string | Original release identifier |
| `source` | string | Source paragraph |
| `source_level` | null | Unavailable in the release |
| `target_level` | string | Normalized `A2` or `B1` |
| `references` | array[string] | Reference list, currently length one |
| `split` | string | `trial` or `test` |

## Generation Records

`member_A_deliverables/data/processed/generation_inputs.jsonl` is intended for
Sankeerth Adisha (B). It has the same identifiers, source, target, and split, but deliberately
excludes `references`.

`member_A_deliverables/data/processed/few_shot_pool.jsonl` contains trial records
only. This is the sole permitted source for in-context examples.

## Prediction Records

Sankeerth Adisha (B) and David Kim (C) should exchange one JSONL object per request:

```json
{
  "id": "21-a2",
  "source_id": "21",
  "split": "test",
  "target_level": "A2",
  "system": "llama_zero_shot",
  "output": "Generated paragraph",
  "seed": 42,
  "revision_count": 0
}
```

Required join key: `id`. Every evaluated system must produce each requested ID
exactly once. `system`, decoding settings, prompt version, and model revision should
also be recorded in an experiment manifest.

## Generated Files

| Path | Consumer | Purpose |
|---|---|---|
| `member_A_deliverables/data/processed/generation_inputs.jsonl` | Sankeerth Adisha (B) | Reference-free model inputs |
| `member_A_deliverables/data/processed/few_shot_pool.jsonl` | Sankeerth Adisha (B) | Permitted demonstrations |
| `member_A_deliverables/data/processed/tsar2025_normalized.jsonl` | David Kim (C) | References and evaluation joins |
| `member_A_deliverables/data/processed/identity_baseline.jsonl` | David Kim (C) | Copy-source baseline |
| `member_A_deliverables/artifacts/eda/dataset_statistics.csv` | Members A/D | Full reproducible EDA |
| `member_A_deliverables/artifacts/eda/dataset_statistics.md` | Shaohua Liu (D) | Paper-ready compact table |
| `member_A_deliverables/artifacts/eda/length_distribution.png` | Shaohua Liu (D) | Paper-ready figure |
| `member_A_deliverables/artifacts/eda/dataset_summary.json` | All | Release counts |
