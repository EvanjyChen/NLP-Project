# Preliminary Paper Plan

## Working Title

**Can Small Open-Weight LLMs Control CEFR Readability? A Preliminary Study of Prompting and Self-Refinement**

## 1. Paper Objective and Scope

The preliminary paper should test one focused claim:

> A lightweight feedback loop using an external CEFR evaluator improves target-level
> compliance for open-weight LLMs, but may trade off meaning preservation.

This framing is narrower and more defensible than attempting to compare every model,
prompt type, metric, and dataset in the proposal. The paper should address:

- **RQ1:** How do direct zero-shot, few-shot, and evaluator-guided self-refinement
  affect CEFR target accuracy?
- **RQ2:** What happens to meaning preservation when CEFR compliance improves?
- **RQ3:** Are the effects different for A2 and B1 targets?

The preliminary report should not claim state-of-the-art performance. Its contribution
is a controlled comparison, a working open-weight pipeline, and an analysis of the
readability-versus-meaning trade-off.

## 2. Corrections Needed Before Drafting

The proposal currently describes the shared-task data as sentence pairs with an
official train/dev/test split. According to the TSAR 2025 task paper, the released
dataset instead contains 100 paragraph-level source texts:

- 20 trial instances for development;
- 80 test instances for official evaluation;
- source levels B2 or C1;
- target levels A2 and B1;
- two target simplifications per source text, for 200 references in total.

The paper must verify the exact structure of the downloaded release before reporting
counts. It must also distinguish the official task metrics from supplementary metrics:

- **Primary:** target CEFR exact accuracy, adjacent accuracy or CEFR RMSE, and
  MeaningBERT semantic similarity;
- **Secondary:** SARI, LENS, FKGL, and BLEU only where their input assumptions are
  satisfied and their limitations are stated;
- **Human check:** adequacy, fluency, and simplicity on a small stratified sample.

ASSET and TurkCorpus are sentence-level, non-CEFR resources. They should not be mixed
into the main TSAR experiment or used as if they were in-domain training data. At most,
use ASSET as a secondary robustness check or a source of generic simplification
demonstrations, with that domain mismatch acknowledged. Omit TurkCorpus from the
preliminary paper unless a concrete cross-dataset result is ready.

The proposal also says the group has four members but names five people/roles. Resolve
the author list and ownership before submission.

## 3. Four-Page Structure

Target approximately 3,200-3,600 words only if the template permits it; figures,
tables, and formatting will usually force a lower count. Keep references outside the
four-page limit as allowed by the instructions.

### Abstract (120-150 words)

State the task, the open-weight model comparison, the three prompt conditions, the
official evaluation dimensions, and one concrete preliminary finding. Write this last.

### 1. Introduction (0.55 page)

1. Motivate CEFR-controlled simplification for accessibility and language learning.
2. Explain that simplification must jointly control readability and preserve meaning.
3. Identify the gap: capable LLMs often need iterative or multi-model pipelines, while
   the reliability of small open-weight models remains uncertain.
4. State RQ1-RQ3.
5. End with two or three factual contributions:
   - a reproducible comparison of three prompting strategies;
   - evaluator-guided self-refinement for small open-weight models;
   - analysis by target level and failure type.

### 2. Related Work (0.9 page)

Organize the 20-24 papers by argument, not one paragraph per paper:

1. **Text simplification data and systems:** establish the standard task, datasets,
   supervised/unsupervised baselines, and common rewrite operations.
2. **Controllable and CEFR-based simplification:** explain explicit control tokens,
   proficiency labels, and why target-level control differs from general simplicity.
3. **LLM prompting and iterative methods:** compare zero/few-shot prompting,
   decomposition, reranking, agents, and feedback loops.
4. **Evaluation:** contrast overlap metrics, learned simplification metrics, CEFR
   prediction, semantic preservation, and human judgment.

Every paragraph should end by stating what prior work leaves unresolved for this
study. Avoid a catalogue of 22 independent summaries.

### 3. Data and Method (0.9 page)

#### Data

Report:

- the official trial/test counts and source/target CEFR distribution;
- paragraph, sentence, and token-length statistics;
- the number of references per source-target pair;
- licensing/access details from the release;
- how trial examples are separated from evaluation examples to avoid leakage.

#### Systems

Use a deliberately small preliminary matrix:

| ID | Model | Prompt condition | Purpose |
|---|---|---|---|
| B0 | Identity/copy | None | Meaning-preserving but non-simplifying floor |
| B1 | One open-weight instruct model | Direct zero-shot | Main simple baseline |
| B2 | Same model | 3-shot, target-level matched | Test in-context examples |
| B3 | Same model | Direct + CEFR feedback, max 2 revisions | Test self-refinement |
| C1 | One second model or proprietary API | Best prompt only | Reference ceiling |

Prefer one model that is already available and runnable in the team environment.
Add the second model only after B0-B3 produce stable outputs. Use deterministic
decoding for the main comparison (`temperature=0` or its API equivalent), a fixed
seed where supported, `max_new_tokens` justified by observed target lengths, and
identical prompts across models apart from chat formatting.

Do not describe hidden chain-of-thought as an experimental condition. If decomposition
is tested, define observable stages such as draft, evaluator feedback, and revision.

#### Self-Refinement

1. Generate a draft for the requested A2 or B1 target.
2. Predict its CEFR level with the official evaluator.
3. If the level misses the target, return only the predicted level plus explicit
   revision instructions to the generator.
4. Stop on a target match or after two revisions.
5. Preserve all intermediate outputs to measure improvement and regression.

### 4. Experiments and Preliminary Results (1.15 pages)

#### Exploratory Data Analysis

Include one compact table with:

- instances by source and target CEFR;
- mean/median source and reference word count;
- mean sentence count;
- lexical diversity or average word length;
- FKGL distribution, clearly labeled as descriptive rather than a CEFR substitute;
- compression ratio from source to reference.

Include one figure only if it reveals a useful pattern. Recommended: paired source and
reference length distributions separated by A2/B1. Put additional EDA in an appendix.

#### Main Evaluation

The main table should report, by system and target level:

- exact CEFR accuracy (higher is better);
- CEFR RMSE or mean absolute level distance (lower is better);
- MeaningBERT source similarity (higher is better);
- SARI or LENS only if successfully validated on paragraph inputs;
- average number of revisions and inference cost for B3.

Use paired bootstrap confidence intervals or a paired randomization test where
possible. With a small test set, report uncertainty and per-instance paired
differences rather than treating small score changes as conclusive.

#### Error Analysis

Stratify 12-20 examples across A2/B1 and success/failure cases. Code failures as:

- target too complex;
- over-simplified;
- omitted essential content;
- hallucinated or altered meaning;
- poor discourse/coreference after sentence splitting;
- ungrammatical or disfluent;
- evaluator-generator disagreement.

Show one short qualitative example containing source, target, baseline output,
self-refined output, predicted CEFR, and a one-sentence analysis.

### 5. Conclusion and Next Steps (0.35 page)

Answer RQ1-RQ3 only to the extent supported by preliminary results. State limitations:
small data, evaluator dependence, prompt sensitivity, paragraph-level metric validity,
and limited human evaluation. Name the exact final-paper extensions: additional
open-weight models, prompt sensitivity across seeds/templates, full human evaluation,
cost analysis, and stronger official-system comparisons.

## 4. Literature Portfolio (22 Papers)

The team should verify each citation against the paper itself and maintain
source-backed notes. A balanced reading set is:

### Foundations, Data, and Baselines

1. Xu et al. (2016), statistical MT for simplification and SARI: defines a standard
   metric and TurkCorpus comparison point.
2. Zhang and Lapata (2017), neural sentence simplification with reinforcement
   learning: representative supervised neural baseline and reward design.
3. Nisioi et al. (2017), neural text simplification: early sequence-to-sequence system
   and evaluation limitations.
4. Alva-Manchego et al. (2020), ASSET: motivates multi-reference evaluation and
   multiple rewrite operations.
5. Martin et al. (2020), ACCESS: foundation for explicit control attributes in
   simplification.
6. Martin et al. (2022), MUSS: establishes an unsupervised simplification baseline.

### Evaluation and Readability Control

7. Sulem et al. (2018), BLEU limitations for simplification: supports using
   task-specific and human evaluation.
8. Maddela et al. (2023), LENS: supplies the learned simplification metric and its
   human-correlation rationale.
9. Kew et al. (2023), BLESS: provides broad LLM simplification comparisons and edit
   analysis.
10. Barayan et al. (2025), zero-shot readability-controlled simplification: closest
    pre-shared-task study of prompt context and readability/meaning trade-offs.
11. Alva-Manchego et al. (2025), TSAR shared-task findings: authoritative source for
    the data, official metrics, systems, and overall conclusions.

### Closest TSAR 2025 Systems

12. Dinç et al. (2025), three-stage CEFR-oriented prompting: direct comparator for
    structured prompting and A2/B1 differences.
13. Vajjala (2025), small models for controlled simplification: closest comparison for
    quantized open-weight models and evaluator feedback.
14. Sanchez-Gomez et al. (2025), lightweight prompt-based models: directly informs
    model size and linguistic-descriptor choices.
15. Arias Russi et al. (2025), multi-agent iterative refinement: comparator for the
    proposed refinement loop, with greater pipeline complexity.
16. Miyata et al. (2025), candidate generation and reranking: winning system and
    evidence for separating readability filtering from semantic ranking.
17. Huynh and Cao (2025), multi-round simplification: evidence that source-target
    readability distance affects iterative performance.
18. Barbu et al. (2025), prompt and LLM-judge comparison: informs prompt ablations and
    evaluator design.
19. Sokova et al. (2025), prompting and reinforcement fine-tuning: contrasts the
    proposed inference-only method with optimization-based adaptation.

### Prompting and Analysis Extensions

20. Ponce et al. (2024), split-and-rephrase with LLMs: relevant to paragraph-level
    sentence splitting, compliance, and meaning preservation.
21. Chernodub et al. (2025), automatic prompt optimization for simplification:
    positions hand-designed prompts against metric-driven prompt search.
22. Shimada et al. (2025), HIT-YOU similarity-based few-shot prompting and
    self-refinement: the closest direct precedent for classifier-feedback refinement,
    making it essential for framing this study as a controlled reproduction and
    open-weight ablation rather than a novel loop.

Assign 5-6 papers to each confirmed group member, but synthesize them under the four
themes above. The shared-task overview and closest systems deserve more space than
generic prompting papers.

## 5. Execution Plan

### Stage 1: Lock the Experimental Contract

- Download and inspect the official data and evaluation scripts.
- Confirm legal access, schema, counts, and evaluator requirements.
- Freeze RQ1-RQ3, the model checkpoint, prompts, decoding settings, and split policy.
- Resolve the group membership inconsistency.

**Exit criterion:** one-page experiment specification reviewed by all authors.

### Stage 2: Produce EDA and Baselines

- Build a dataset validation/EDA script.
- Run identity, zero-shot, and reference-oracle sanity checks.
- Verify evaluator outputs on official references.
- Save predictions and metadata in a stable tabular format.

**Exit criterion:** reproducible EDA table and at least B0-B1 result rows.

### Stage 3: Run Preliminary Ablations

- Add 3-shot prompting with examples chosen only from permitted development data.
- Add the maximum-two-step feedback loop.
- Run paired evaluation and record cost/latency.
- Freeze preliminary outputs before qualitative analysis.

**Exit criterion:** complete B0-B3 table with no missing predictions.

### Stage 4: Analyze and Draft

- Sample error-analysis cases using a fixed stratification rule.
- Draft Data/Method and Results first, then Related Work and Introduction.
- Create one main result table, one EDA table, and at most one figure/example.
- Conduct an internal claim-evidence audit: every claim must point to a result or
  citation.

**Exit criterion:** four-page template-compliant draft with all numbers generated by
versioned scripts.

### Stage 5: Final Checks

- Confirm the template and page count before prose polishing.
- Check references, author names, dataset/model versions, and metric directionality.
- Have every member explain the pipeline and one assigned literature theme.
- Move secondary details, prompts, extra examples, and full EDA to the appendix.

## 6. Suggested Ownership

After confirming the actual four-person author list, assign one primary owner and one
reviewer to each artifact:

| Artifact | Primary role | Required reviewer |
|---|---|---|
| Data validation and EDA | Data lead | Evaluation lead |
| Prompting and refinement pipeline | Method lead | Baseline lead |
| Baselines and metric harness | Evaluation lead | Method lead |
| Literature synthesis and human/error analysis | Writing lead | Data lead |
| Tables, figures, and template integration | Writing lead | Entire team |

Ownership should follow artifacts rather than paper sections: all authors remain
responsible for understanding the complete study.

## 7. Minimum Submission Standard

The preliminary paper is ready only when it contains:

- the required conference/workshop template and no more than four main-text pages;
- 20-24 verified, contextualized papers;
- correct official dataset statistics;
- one reproducible open-weight baseline with actual results;
- one meaningful comparison against that baseline;
- EDA grounded in the released data;
- CEFR compliance and semantic-preservation measurements;
- uncertainty or an explicit small-sample caveat;
- qualitative failure analysis;
- clearly stated limitations and final-paper next steps.
