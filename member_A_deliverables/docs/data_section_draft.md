# Data Section Draft

> LLM-assisted draft. Verify all facts, figures, and citations before submission.

We use the public English data release associated with the TSAR 2025 Shared Task on
Readability-Controlled Text Simplification (Alva-Manchego et al., 2025). Its inputs
are paragraph-length pedagogical texts, each paired with requests for A2 and B1
simplifications under the Common European Framework of Reference. We pin the trial
and test repositories to specific revisions and retain the raw JSONL files unchanged.
The downloaded release contains 40 trial requests derived from 20 unique source
paragraphs and 200 test requests derived from 100 unique sources. Each request has
one reference simplification. These counts differ from the 80-test-source figure in
the shared-task paper, so we report both the repository revisions and counts observed
in the files used for our experiments.

We reserve trial references for prompt development and in-context demonstrations.
Test references are removed from the model-facing input file and used only after
test outputs have been frozen. This separation prevents reference leakage despite
their presence in the current public test release. The release does not provide
per-record source CEFR labels; therefore, we describe the sources as B2 or above
following the task documentation without assigning an inferred source label.

Across all 120 unique sources, paragraphs contain 85.96 words on average. A2
references average 74.05 words and 5.77 sentences, whereas B1 references average
82.09 words and 4.93 sentences. Their mean source-normalized length ratios are 0.874
and 0.966, respectively. A heuristic Flesch-Kincaid calculation also separates the
targets (5.80 for A2 and 8.59 for B1), but we use it only for descriptive analysis,
not as a substitute for the official CEFR evaluator. The dataset is small and drawn
from pedagogical material, which limits statistical power and domain generalization.
