# Sankeerth Adisha (B) Handoff: Prompting and Self-Refinement Pipeline

## Objective

Implement a reproducible generation pipeline for direct zero-shot, three-shot, and
CEFR-feedback self-refinement conditions using one open-weight instruction model.
Produce frozen prediction files that David Kim (C) can evaluate without manual cleanup.
Sankeerth Adisha (B) owns the generation-time CEFR critic locally and does not call
any service maintained by David Kim (C).

Do not expand to additional models until the first model completes all three
conditions successfully.

## Inputs

Read:

- `member_A_deliverables/data/processed/generation_inputs.jsonl`
- `member_A_deliverables/data/processed/few_shot_pool.jsonl`
- `member_A_deliverables/docs/data_schema.md`
- `member_A_deliverables/docs/split_policy.md`
- `member_A_deliverables/docs/data_source.md`

Do not read `tsar2025_normalized.jsonl` or raw test data in generation code. Those
files contain test references.

## Dependency Contract with David Kim

Sankeerth and David work independently until the final prediction handoff:

1. Sankeerth can complete zero-shot, three-shot, and self-refinement without any code
   or service from David. Self-refinement uses Sankeerth's local CEFR critic.
2. David can build and test the complete evaluation harness using identity and
   synthetic predictions without waiting for Sankeerth.
3. The only required handoff is one-way: after generation is complete, Sankeerth
   gives David the frozen files under `member_B_deliverables/predictions/`, their
   manifests, and SHA-256 hashes.
4. David validates those hashes and independently computes final CEFR and semantic
   scores. David does not copy Sankeerth's local critic scores.
5. Sankeerth never receives test references from David, and David never edits
   Sankeerth's prediction files.

Sankeerth's task is complete before David's final scoring begins. David's only
dependency on Sankeerth is the final frozen prediction bundle.

## Required Output Directory

Create:

```text
member_B_deliverables/
  README.md
  prompts/
    direct_v1.txt
    few_shot_v1.txt
    refine_v1.txt
  scripts/
  tests/
  critic/
    manifest.json
    cache/
  predictions/
    identity_or_smoke.jsonl
    zero_shot.jsonl
    three_shot.jsonl
    self_refine.jsonl
  manifests/
    zero_shot.json
    three_shot.json
    self_refine.json
  logs/
```

Do not write generated files inside `member_A_deliverables/`.

## Implementation Tasks

### B-01: Input and Output Validation

- Load JSONL using structured parsing.
- Require unique input IDs and non-empty source text.
- Validate every output against the prediction schema.
- Reject missing, duplicate, unknown, or empty outputs.
- Preserve `id`, `source_id`, `split`, and `target_level` exactly.

### B-02: Model Adapter

- Make model ID, revision, quantization, device, and batch size configurable.
- Start with one available open-weight instruction checkpoint.
- Keep model-specific chat formatting inside one adapter.
- Use deterministic decoding for the main run where supported:
  `do_sample=false`, fixed seed, and a documented token limit.
- Record the exact model and library revisions in each manifest.

### B-03: Direct Zero-Shot

- Use one concise level-aware instruction.
- Ask for only the simplified paragraph, with no explanation or analysis.
- Use identical prompt semantics for A2 and B1; vary only the target descriptor.
- Strip chat wrappers but do not silently rewrite model content.

### B-04: Three-Shot Prompting

- Draw demonstrations only from `few_shot_pool.jsonl`.
- Match demonstration target level to the current request.
- Select exactly three unique source IDs using a deterministic rule.
- Freeze and record selected IDs and their order.
- If evaluating trial inputs, exclude the current `source_id` from demonstrations.

### B-05: Self-Refinement

- Generate the direct draft first.
- Load one fixed organizer-published CEFR checkpoint inside Sankeerth's pipeline as
  the generation-time critic. Prefer the document-level checkpoint after verifying
  its model card.
- Pin the critic checkpoint revision, label mapping, library versions, and inference
  settings in `critic/manifest.json`.
- Cache critic predictions so interrupted runs can resume deterministically.
- If predicted level differs from the requested level, revise using only:
  target level, predicted level, source, and previous output.
- Never provide a test reference to the model.
- Stop on target match or after two revisions.
- Preserve every intermediate draft and local critic response in logs.
- Final predictions must include the number of completed revisions.
- Treat critic scores as generation metadata only. David Kim (C) will independently
  recompute final CEFR metrics and must not reuse these scores.

Expected local critic record:

```json
{
  "id": "21-a2",
  "iteration": 0,
  "target_level": "A2",
  "predicted_level": "B1",
  "confidence": 0.81,
  "target_match": false
}
```

Use a fake critic in unit tests so development requires neither David nor a neural
model download.

### B-06: Smoke and Full Runs

1. Run two A2 and two B1 trial requests.
2. Confirm output-only formatting and deterministic reruns.
3. Run all trial requests.
4. Freeze prompts and settings.
5. Run all test requests.
6. Hash each prediction and manifest file.

## Prediction Contract

Each final JSONL row must contain:

```json
{
  "id": "21-a2",
  "source_id": "21",
  "split": "test",
  "target_level": "A2",
  "system": "open_model_zero_shot",
  "output": "Simplified paragraph",
  "seed": 42,
  "revision_count": 0
}
```

Intermediate self-refinement records belong in logs, not the final prediction file.

## Minimum Tests

- Input duplicate IDs are rejected.
- Output missing IDs and extra IDs are rejected.
- Empty model output is rejected.
- Three-shot selection returns three unique, target-matched trial examples.
- Trial evaluation never selects its own source as a demonstration.
- Test references cannot enter the prompt-building interface.
- The local critic accepts only candidate text and target metadata, never references.
- Self-refinement stops on a match.
- Self-refinement stops after two revisions on repeated misses.
- Same seed/settings produce identical prompts and manifests.

## Definition of Done

- Zero-shot, three-shot, and self-refinement files cover every requested test ID once.
- Prompts and manifests fully reproduce each condition.
- The generation-time critic checkpoint and cache are reproducible.
- No test reference is read by generation code.
- Tests pass and a four-record smoke run is documented.
- David Kim (C) can validate predictions without changing their format.

## LLM Implementation Prompt

Use the following as the initial instruction for a coding LLM:

```text
You are Sankeerth Adisha (B) for an NLP research project. Implement the prompting and
self-refinement pipeline described in
member_A_deliverables/handoffs/member_B_prompting_pipeline.md.

First read:
- member_A_deliverables/docs/data_schema.md
- member_A_deliverables/docs/split_policy.md
- the two permitted JSONL inputs for Sankeerth

Create all work under member_B_deliverables/. Do not modify Member A files and do not
read reference-bearing test files in production generation code. Use test-first,
configurable Python code. Sankeerth owns a fixed generation-time CEFR critic and must
not depend on David at runtime. Start with data validation plus a fake model and fake
critic so tests run without GPU or network access. Then add one real open-weight model
adapter and one pinned organizer-published CEFR checkpoint. Keep critic scores as
generation metadata; David will independently recompute final metrics. Run the
smallest tests after each step and finish with a four-record smoke run. Report files
changed, commands run, and anything requiring model credentials or GPU.
```
