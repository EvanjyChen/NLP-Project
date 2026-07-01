#!/usr/bin/env python3
"""Validate, normalize, and summarize the TSAR 2025 shared-task data."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any

DELIVERABLE_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_FIELDS = {
    "dataset_id",
    "text_id",
    "original",
    "target_cefr",
    "reference",
}
EXPECTED_TARGETS = {"A2", "B1"}
WORD_RE = re.compile(r"[A-Za-z]+(?:['’-][A-Za-z]+)*|\d+(?:[.,]\d+)*")
SENTENCE_RE = re.compile(r"[.!?]+(?:[\"')\]]+)?(?:\s+|$)")
ID_RE = re.compile(r"^(?P<source_id>.+)-(?P<target>a2|b1)$", re.IGNORECASE)
VOWELS = set("aeiouy")


class DataValidationError(ValueError):
    """Raised when released data violates the expected shared-task contract."""


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as error:
                raise DataValidationError(
                    f"{path}:{line_number}: malformed JSON: {error.msg}"
                ) from error
            if not isinstance(value, dict):
                raise DataValidationError(
                    f"{path}:{line_number}: each line must be a JSON object"
                )
            records.append(value)
    return records


def _normalize_record(
    raw: dict[str, Any], split: str, line_number: int
) -> dict[str, Any]:
    missing = EXPECTED_FIELDS - raw.keys()
    if missing:
        names = ", ".join(sorted(missing))
        raise DataValidationError(f"line {line_number}: missing fields: {names}")

    for field in EXPECTED_FIELDS:
        if not isinstance(raw[field], str):
            raise DataValidationError(f"line {line_number}: {field} must be a string")
        if not raw[field].strip():
            raise DataValidationError(f"line {line_number}: empty {field}")

    text_id = raw["text_id"].strip()
    match = ID_RE.fullmatch(text_id)
    if not match:
        raise DataValidationError(
            f"line {line_number}: text_id must end in -a2 or -b1"
        )

    target = raw["target_cefr"].strip().upper()
    if target not in EXPECTED_TARGETS:
        raise DataValidationError(
            f"line {line_number}: unsupported target CEFR {target!r}"
        )
    if match.group("target").upper() != target:
        raise DataValidationError(
            f"line {line_number}: text_id {text_id!r} does not match target {target}"
        )

    return {
        "id": text_id.lower(),
        "source_id": match.group("source_id"),
        "dataset_id": raw["dataset_id"].strip(),
        "source": raw["original"].strip(),
        "source_level": None,
        "target_level": target,
        "references": [raw["reference"].strip()],
        "split": split,
    }


def load_and_validate(path: Path, split: str) -> list[dict[str, Any]]:
    """Load one released split and enforce IDs, labels, pairs, and text integrity."""
    if split not in {"trial", "test"}:
        raise DataValidationError(f"unsupported split {split!r}")

    normalized = [
        _normalize_record(raw, split, line_number)
        for line_number, raw in enumerate(_read_jsonl(path), start=1)
    ]
    if not normalized:
        raise DataValidationError(f"{path}: dataset is empty")

    ids: set[str] = set()
    sources: dict[str, str] = {}
    targets_by_source: dict[str, set[str]] = defaultdict(set)
    for record in normalized:
        record_id = str(record["id"])
        if record_id in ids:
            raise DataValidationError(f"duplicate id: {record_id}")
        ids.add(record_id)

        source_id = str(record["source_id"])
        source = str(record["source"])
        if source_id in sources and sources[source_id] != source:
            raise DataValidationError(
                f"source_id {source_id!r} maps to inconsistent original text"
            )
        sources[source_id] = source
        targets_by_source[source_id].add(str(record["target_level"]))

    incomplete = {
        source_id: sorted(targets)
        for source_id, targets in targets_by_source.items()
        if targets != EXPECTED_TARGETS
    }
    if incomplete:
        raise DataValidationError(f"incomplete A2/B1 source pairs: {incomplete}")

    return normalized


def _count_syllables(word: str) -> int:
    letters = re.sub(r"[^a-z]", "", word.lower())
    if not letters:
        return 0
    groups = 0
    previous_was_vowel = False
    for letter in letters:
        is_vowel = letter in VOWELS
        if is_vowel and not previous_was_vowel:
            groups += 1
        previous_was_vowel = is_vowel
    if letters.endswith("e") and groups > 1 and not letters.endswith(("le", "ye")):
        groups -= 1
    return max(groups, 1)


def compute_text_metrics(text: str) -> dict[str, float | int]:
    """Return deterministic surface statistics and a heuristic FKGL estimate."""
    words = WORD_RE.findall(text)
    if not words:
        raise DataValidationError("cannot compute metrics for text without words")
    sentence_count = len(SENTENCE_RE.findall(text))
    sentence_count = max(sentence_count, 1)
    normalized_words = [word.lower() for word in words]
    syllable_count = sum(_count_syllables(word) for word in words)
    word_count = len(words)
    fkgl = (
        0.39 * (word_count / sentence_count)
        + 11.8 * (syllable_count / word_count)
        - 15.59
    )
    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "average_word_length": sum(len(word) for word in words) / word_count,
        "type_token_ratio": len(set(normalized_words)) / word_count,
        "fkgl": fkgl,
    }


def _mean(values: list[float]) -> float:
    return statistics.fmean(values) if values else math.nan


def _summarize_texts(
    split: str,
    group: str,
    texts: list[str],
    compression_ratios: list[float],
) -> dict[str, str | int | float]:
    metrics = [compute_text_metrics(text) for text in texts]
    words = [float(item["word_count"]) for item in metrics]
    sentences = [float(item["sentence_count"]) for item in metrics]
    return {
        "split": split,
        "group": group,
        "n": len(texts),
        "mean_words": _mean(words),
        "median_words": statistics.median(words),
        "mean_sentences": _mean(sentences),
        "median_sentences": statistics.median(sentences),
        "mean_average_word_length": _mean(
            [float(item["average_word_length"]) for item in metrics]
        ),
        "mean_type_token_ratio": _mean(
            [float(item["type_token_ratio"]) for item in metrics]
        ),
        "mean_fkgl_heuristic": _mean([float(item["fkgl"]) for item in metrics]),
        "mean_compression_ratio": _mean(compression_ratios),
    }


def build_statistics(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build paper-ready source/reference summaries by split and target level."""
    summaries: list[dict[str, Any]] = []
    split_names = sorted({str(record["split"]) for record in records})
    for split in [*split_names, "all"]:
        selected = (
            records
            if split == "all"
            else [record for record in records if record["split"] == split]
        )
        source_by_id = {
            f"{record['split']}:{record['source_id']}": str(record["source"])
            for record in selected
        }
        summaries.append(
            _summarize_texts(split, "Sources", list(source_by_id.values()), [])
        )
        for target in sorted(EXPECTED_TARGETS):
            target_records = [
                record for record in selected if record["target_level"] == target
            ]
            references = [str(record["references"][0]) for record in target_records]
            ratios = [
                compute_text_metrics(str(record["references"][0]))["word_count"]
                / compute_text_metrics(str(record["source"]))["word_count"]
                for record in target_records
            ]
            summaries.append(
                _summarize_texts(
                    split, f"{target} references", references, ratios
                )
            )
    return summaries


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def _write_statistics(
    csv_path: Path, markdown_path: Path, summaries: list[dict[str, Any]]
) -> None:
    fieldnames = list(summaries[0])
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summaries)

    paper_rows = [row for row in summaries if row["split"] == "all"]
    lines = [
        "| Group | N | Mean words | Median words | Mean sentences | "
        "FKGL (heuristic) | Compression ratio |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in paper_rows:
        compression = row["mean_compression_ratio"]
        compression_text = (
            "n/a"
            if isinstance(compression, float) and math.isnan(compression)
            else f"{float(compression):.3f}"
        )
        lines.append(
            f"| {row['group']} | {row['n']} | {float(row['mean_words']):.2f} | "
            f"{float(row['median_words']):.2f} | "
            f"{float(row['mean_sentences']):.2f} | "
            f"{float(row['mean_fkgl_heuristic']):.2f} | {compression_text} |"
        )
    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_figure(path: Path, records: list[dict[str, Any]]) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    source_by_id = {
        f"{record['split']}:{record['source_id']}": str(record["source"])
        for record in records
    }
    groups = {
        "Sources": [
            compute_text_metrics(text)["word_count"]
            for text in source_by_id.values()
        ],
        "A2 references": [
            compute_text_metrics(str(record["references"][0]))["word_count"]
            for record in records
            if record["target_level"] == "A2"
        ],
        "B1 references": [
            compute_text_metrics(str(record["references"][0]))["word_count"]
            for record in records
            if record["target_level"] == "B1"
        ],
    }
    figure, axis = plt.subplots(figsize=(7.2, 4.2))
    axis.boxplot(
        list(groups.values()),
        tick_labels=list(groups),
        showmeans=True,
        meanline=True,
    )
    axis.set_ylabel("Word count")
    axis.set_title("TSAR 2025 paragraph lengths")
    axis.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    figure.savefig(path, dpi=180)
    plt.close(figure)


def run_pipeline(
    trial_path: Path,
    test_path: Path,
    processed_dir: Path,
    artifacts_dir: Path,
) -> dict[str, int]:
    """Run validation and generate all Member A handoff artifacts."""
    trial = load_and_validate(trial_path, "trial")
    test = load_and_validate(test_path, "test")

    trial_sources = {str(record["source"]) for record in trial}
    test_sources = {str(record["source"]) for record in test}
    overlap = trial_sources & test_sources
    if overlap:
        raise DataValidationError(
            f"cross-split source overlap detected for {len(overlap)} texts"
        )

    processed_dir.mkdir(parents=True, exist_ok=True)
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    records = [*trial, *test]
    _write_jsonl(processed_dir / "tsar2025_normalized.jsonl", records)
    generation_inputs = [
        {
            "id": record["id"],
            "source_id": record["source_id"],
            "dataset_id": record["dataset_id"],
            "source": record["source"],
            "source_level": record["source_level"],
            "target_level": record["target_level"],
            "split": record["split"],
        }
        for record in records
    ]
    _write_jsonl(processed_dir / "generation_inputs.jsonl", generation_inputs)
    _write_jsonl(processed_dir / "few_shot_pool.jsonl", trial)

    identity = [
        {
            "id": record["id"],
            "source_id": record["source_id"],
            "split": record["split"],
            "target_level": record["target_level"],
            "system": "identity",
            "output": record["source"],
            "seed": None,
            "revision_count": 0,
        }
        for record in records
    ]
    _write_jsonl(processed_dir / "identity_baseline.jsonl", identity)

    summaries = build_statistics(records)
    _write_statistics(
        artifacts_dir / "dataset_statistics.csv",
        artifacts_dir / "dataset_statistics.md",
        summaries,
    )
    _write_figure(artifacts_dir / "length_distribution.png", records)

    source_keys = {
        f"{record['split']}:{record['source_id']}" for record in records
    }
    summary = {
        "trial_requests": len(trial),
        "test_requests": len(test),
        "total_requests": len(records),
        "unique_sources": len(source_keys),
    }
    (artifacts_dir / "dataset_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--trial",
        type=Path,
        default=DELIVERABLE_ROOT / "data/raw/tsar2025_trial.jsonl",
    )
    parser.add_argument(
        "--test",
        type=Path,
        default=DELIVERABLE_ROOT / "data/raw/tsar2025_test.jsonl",
    )
    parser.add_argument(
        "--processed-dir",
        type=Path,
        default=DELIVERABLE_ROOT / "data/processed",
    )
    parser.add_argument(
        "--artifacts-dir",
        type=Path,
        default=DELIVERABLE_ROOT / "artifacts/eda",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_pipeline(
        trial_path=args.trial,
        test_path=args.test,
        processed_dir=args.processed_dir,
        artifacts_dir=args.artifacts_dir,
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
