# Split and Leakage Policy

## Main Rule

Use trial references for development and demonstrations. Use test sources for the
main evaluation. Do not expose test references to model generation, prompt selection,
candidate selection, stopping rules, or hyperparameter tuning.

## Permitted Uses

| Resource | Prompt development | Few-shot examples | Model generation | Final evaluation |
|---|---:|---:|---:|---:|
| Trial sources | Yes | Yes | Yes | Optional diagnostic |
| Trial references | Yes | Yes | No direct copying | Yes |
| Test sources | No prompt tuning | No | Yes | Yes |
| Test references | No | No | No | Yes, after outputs are frozen |

Sankeerth Adisha (B) should read `generation_inputs.jsonl`, which excludes references. David Kim (C)
may read `tsar2025_normalized.jsonl` when scoring frozen outputs.

## Few-Shot Selection

- Select examples only from `few_shot_pool.jsonl`.
- Freeze the selection rule before looking at test scores.
- Record the exact demonstration IDs and order for every run.
- If reporting trial-set scores from a few-shot system, exclude the evaluated
  source from its own prompt. Prefer leave-one-source-out selection.
- Do not choose demonstrations by comparing their references to a test reference.

## Test Procedure

1. Freeze prompt text, model revision, decoding settings, and demonstration rule.
2. Generate all test outputs from reference-free inputs.
3. Validate that every ID appears exactly once and no output is empty.
4. Save immutable output files and hashes.
5. Only then join outputs with test references and run evaluation.

## EDA

References from both public splits may be used for aggregate EDA because EDA does not
produce model outputs. However, observations from test references must not be used to
tune generation settings. The cleanest preliminary-paper protocol is to use release
wide EDA descriptively, trial for development, and test for frozen evaluation.

