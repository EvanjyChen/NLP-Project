# TSAR 2025 Data Source and Provenance

## Official Sources

The data was downloaded on 2026-07-01 from the Cardiff NLP Hugging Face
collection associated with the TSAR 2025 shared-task organizers:

- Collection:
  https://huggingface.co/collections/cardiffnlp/tsar-2025-shared-task-on-rcts
- Trial repository:
  https://huggingface.co/datasets/cardiffnlp/TSAR2025_SharedTask_RCTS_Trial-Data
- Test repository:
  https://huggingface.co/datasets/cardiffnlp/TSAR2025_SharedTask_RCTS_Test-Data
- Shared-task paper:
  https://aclanthology.org/2025.tsar-1.8/

The raw files are pinned to repository revisions rather than a moving `main`
branch:

| Split | Repository revision | File | SHA-256 |
|---|---|---|---|
| Trial | `c4d590b66dbb5dbd31c8a158f068c0adcfbe0af3` | `tsar2025_trial.jsonl` | `4a9e32c55eb85fc31dd50c7cc5ce0ee210176b31edc7f0fd7c10eaed3a786de0` |
| Test | `3f4a9d38f82eb9126c2a069f0bd009301fb3df28` | `tsar2025_test.jsonl` | `c3df44e22c5e353008d4d40f20342d28f279662d2df0d56771cadf84b798f380` |

The repository README files are retained beside the JSONL files in
`member_A_deliverables/data/raw/`.

## Verified Release Statistics

Counts below come from the downloaded files, not from the proposal:

| Split | Generation requests | Unique source paragraphs | A2 requests | B1 requests | References per request |
|---|---:|---:|---:|---:|---:|
| Trial | 40 | 20 | 20 | 20 | 1 |
| Test | 200 | 100 | 100 | 100 | 1 |
| Total | 240 | 120 | 120 | 120 | 1 |

Each unique source appears once with target A2 and once with target B1. The release
does not include a source CEFR field. The task description characterizes sources as
B2 or above, but that statement must not be converted into per-record labels.

## Documented Discrepancies

- The project proposal incorrectly claims a sentence-level train/dev/test corpus.
  The public files contain paragraph-level `trial` and `test` splits and no training
  split.
- The shared-task paper describes 20 trial and 80 test source texts, whereas the
  current public release contains 20 trial and 100 test source texts. Report the
  exact release revision and both request/source counts in the paper.
- The task website mentions A1, A2, or B1 in one description, but the released files
  contain only A2 and B1 targets.
- The current public test file includes references. They must remain unavailable to
  the generation pipeline and be used only for post-generation evaluation.

## Evaluation Resources

The official Hugging Face collection contains three CEFR evaluator checkpoints:

- `AbdullahBarayan/ModernBERT-base-doc_sent_en-Cefr`
- `AbdullahBarayan/ModernBERT-base-doc_en-Cefr`
- `AbdullahBarayan/ModernBERT-base-reference_AllLang2-Cefr2`

No standalone official evaluation-script repository was linked from the current
public collection or task page. A participant repository,
`hulat-group/tsar_2025_workshop`, contains a `metrics/TSAR2025_metrics.py` file, but it
is a third-party system repository and must not be described as the authoritative
organizer release without further confirmation.

## License and Redistribution

The Hugging Face dataset cards currently do not declare a dataset license. The
shared-task paper says the organizers obtained permission to use and distribute the
British Council material for research, but this does not establish a general reuse
license in the local project. Before publishing or redistributing the raw texts,
confirm terms with the organizers. Derived aggregate statistics are safer to share
than copied source/reference paragraphs.
