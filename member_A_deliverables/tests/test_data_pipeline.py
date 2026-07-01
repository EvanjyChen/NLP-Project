import json
from pathlib import Path

import pytest

from member_A_deliverables.scripts.data_pipeline import (
    DataValidationError,
    compute_text_metrics,
    load_and_validate,
    run_pipeline,
)


def write_jsonl(path: Path, rows: list[dict[str, str]]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def make_rows(dataset_id: str, start: int = 1) -> list[dict[str, str]]:
    source = (
        f"Engineers designed bridge {start} to resist strong earthquakes."
    )
    return [
        {
            "dataset_id": dataset_id,
            "text_id": f"{start:02d}-a2",
            "original": source,
            "target_cefr": "a2",
            "reference": "Engineers made the bridge safe during earthquakes.",
        },
        {
            "dataset_id": dataset_id,
            "text_id": f"{start:02d}-b1",
            "original": source,
            "target_cefr": "B1",
            "reference": "Engineers designed the bridge to stay safe in earthquakes.",
        },
    ]


def test_load_and_normalize_valid_records(tmp_path: Path) -> None:
    path = tmp_path / "trial.jsonl"
    write_jsonl(path, make_rows("trial"))

    records = load_and_validate(path, "trial")

    assert [record["id"] for record in records] == ["01-a2", "01-b1"]
    assert [record["target_level"] for record in records] == ["A2", "B1"]
    assert all(record["source_id"] == "01" for record in records)
    assert all(record["split"] == "trial" for record in records)
    assert records[0]["references"] == [
        "Engineers made the bridge safe during earthquakes."
    ]


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (lambda rows: rows[0].pop("reference"), "missing fields"),
        (
            lambda rows: rows[0].update(target_cefr="B1"),
            "does not match target",
        ),
        (lambda rows: rows.append(rows[0].copy()), "duplicate id"),
        (lambda rows: rows[0].update(reference=""), "empty reference"),
    ],
)
def test_invalid_records_are_rejected(
    tmp_path: Path,
    mutate: object,
    message: str,
) -> None:
    rows = make_rows("trial")
    mutate(rows)  # type: ignore[operator]
    path = tmp_path / "invalid.jsonl"
    write_jsonl(path, rows)

    with pytest.raises(DataValidationError, match=message):
        load_and_validate(path, "trial")


def test_text_metrics_are_deterministic() -> None:
    metrics = compute_text_metrics("Cats sleep. Dogs run quickly!")

    assert metrics["word_count"] == 5
    assert metrics["sentence_count"] == 2
    assert metrics["average_word_length"] == pytest.approx(4.6)
    assert metrics["type_token_ratio"] == 1.0
    assert metrics["fkgl"] == pytest.approx(metrics["fkgl"], abs=0)


def test_pipeline_generates_handoff_artifacts(tmp_path: Path) -> None:
    raw = tmp_path / "raw"
    processed = tmp_path / "processed"
    artifacts = tmp_path / "artifacts"
    raw.mkdir()
    write_jsonl(raw / "trial.jsonl", make_rows("trial", 1))
    write_jsonl(raw / "test.jsonl", make_rows("test", 2))

    summary = run_pipeline(
        trial_path=raw / "trial.jsonl",
        test_path=raw / "test.jsonl",
        processed_dir=processed,
        artifacts_dir=artifacts,
    )

    assert summary["trial_requests"] == 2
    assert summary["test_requests"] == 2
    assert summary["unique_sources"] == 2
    assert (processed / "tsar2025_normalized.jsonl").is_file()
    assert (processed / "identity_baseline.jsonl").is_file()
    generation_rows = [
        json.loads(line)
        for line in (processed / "generation_inputs.jsonl").read_text().splitlines()
    ]
    assert all("references" not in row for row in generation_rows)
    few_shot_rows = [
        json.loads(line)
        for line in (processed / "few_shot_pool.jsonl").read_text().splitlines()
    ]
    assert {row["split"] for row in few_shot_rows} == {"trial"}
    assert (artifacts / "dataset_statistics.csv").is_file()
    assert (artifacts / "dataset_statistics.md").is_file()
    assert (artifacts / "length_distribution.png").stat().st_size > 0


def test_pipeline_rejects_cross_split_source_leakage(tmp_path: Path) -> None:
    raw = tmp_path / "raw"
    raw.mkdir()
    rows = make_rows("trial", 1)
    write_jsonl(raw / "trial.jsonl", rows)
    write_jsonl(raw / "test.jsonl", rows)

    with pytest.raises(DataValidationError, match="cross-split source overlap"):
        run_pipeline(
            trial_path=raw / "trial.jsonl",
            test_path=raw / "test.jsonl",
            processed_dir=tmp_path / "processed",
            artifacts_dir=tmp_path / "artifacts",
        )
