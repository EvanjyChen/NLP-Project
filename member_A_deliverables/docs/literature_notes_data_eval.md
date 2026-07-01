# Data and Evaluation Literature Worksheet

> These are source-backed notes for the Related Work section. Verify the summaries
> against the cited papers before submission.

## Alva-Manchego et al. (2025): TSAR Shared-Task Findings

- **Source:** https://aclanthology.org/2025.tsar-1.8/
- **Question:** How should systems simplify English pedagogical paragraphs to a
  requested CEFR level while preserving meaning?
- **Data:** Teacher-produced A2/B1 simplifications of B2/C1 pedagogical texts.
- **Method:** Shared-task comparison of 48 submissions from 20 teams.
- **Metrics:** CEFR evaluator predictions, MeaningBERT source/reference similarity,
  and AUTORANK aggregation.
- **Finding:** LLM systems perform strongly, but dependable control commonly uses
  iterative generation, reranking, agents, or external evaluation.
- **Limitation:** Automatic metrics appear close to saturation and may not represent
  practical human usefulness.
- **Project link:** Defines our task, release, official evaluation dimensions, and
  strongest direct comparators.

## Alva-Manchego et al. (2020): ASSET

- **Source:** https://aclanthology.org/2020.acl-main.424/
- **Question:** Can a multi-reference benchmark represent the range of valid
  simplification operations better than lexically focused datasets?
- **Data:** Crowdsourced English simplifications with multiple references per source.
- **Method:** Annotators apply paraphrasing, deletion, sentence splitting, and
  reordering; the paper compares resulting corpus properties and metric behavior.
- **Metrics:** Human judgments and standard simplification metrics including SARI and
  BLEU.
- **Finding:** ASSET references are more abstractive and capture a broader range of
  transformations than earlier evaluation corpora.
- **Limitation:** It is sentence-level, Wikipedia-derived, and not CEFR controlled.
- **Project link:** Useful as secondary context, but its domain and control labels do
  not match the paragraph-level TSAR experiment.

## Xu et al. (2016): SARI

- **Source:** https://aclanthology.org/Q16-1029/
- **Question:** How can statistical machine translation be tuned and evaluated for
  text simplification rather than generic translation?
- **Data:** Large-scale paraphrases plus manually simplified, multi-reference data
  used for system optimization and evaluation.
- **Method:** Adapts statistical MT and introduces SARI to score additions, deletions,
  and retained n-grams against source and references.
- **Metrics:** SARI and comparison metrics, supported by human evaluation.
- **Finding:** A simplification-specific objective supports more useful tuning and
  evaluation than translation overlap alone.
- **Limitation:** Reference overlap remains sensitive to the available
  simplifications and does not directly measure CEFR compliance.
- **Project link:** Supports SARI as a supplementary metric, not the primary official
  metric for TSAR.

## Sulem et al. (2018): BLEU Is Not Suitable

- **Source:** https://aclanthology.org/D18-1081/
- **Question:** Does BLEU reflect human judgments when systems perform structural
  simplification such as sentence splitting?
- **Data:** A manually constructed sentence-splitting gold-standard corpus with
  structural paraphrases.
- **Method:** Correlates BLEU with human grammaticality, meaning, and simplicity
  judgments.
- **Finding:** BLEU has low or no correlation with grammaticality and meaning when
  splitting occurs and can correlate negatively with simplicity.
- **Limitation:** The analysis focuses particularly on sentence splitting rather than
  every simplification setting.
- **Project link:** Justifies not treating BLEU as a main result for paragraph-level
  outputs that may split sentences.

## Maddela et al. (2023): LENS

- **Source:** https://aclanthology.org/2023.acl-long.905/
- **Question:** Can a learned metric trained on diverse human judgments evaluate
  modern simplification systems more reliably?
- **Data:** SimpEval-past has about 12,000 ratings of 2,400 outputs from 24 systems;
  SimpEval-2022 has more than 1,000 ratings of 360 outputs including GPT-3.5.
- **Method:** Trains LENS on human ratings and introduces list-wise Rank & Rate human
  evaluation.
- **Finding:** LENS correlates with human judgments better than prior automatic
  metrics in the reported experiments.
- **Limitation:** Training judgments and benchmarks are not designed specifically for
  paragraph-level CEFR compliance.
- **Project link:** LENS may supplement official metrics after paragraph-input
  validity is checked; it cannot replace the CEFR evaluator.

## Barayan et al. (2025): Zero-Shot RCTS

- **Source:** https://aclanthology.org/2025.coling-main.452/
- **Question:** How does prompt context affect zero-shot readability control, and what
  trade-off exists between target readability and meaning preservation?
- **Data:** Sentence-level readability-controlled simplification benchmarks.
- **Method:** Evaluates instruction-tuned LLMs with different contextual information
  using automatic and manual analysis.
- **Metrics:** Readability/target control, meaning preservation, and human judgments.
- **Finding:** Models struggle most at the lowest target levels; source properties
  can prevent adequate rewriting, and standard metrics may misread valid edits.
- **Limitation:** The study is sentence-level and predates the paragraph-level TSAR
  shared-task release.
- **Project link:** Directly motivates separate A2/B1 reporting and analysis of the
  control-versus-meaning trade-off.
