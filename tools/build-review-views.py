from __future__ import annotations

import csv
import datetime
import hashlib
import io
import json
import pathlib


REPO = pathlib.Path(__file__).resolve().parent.parent
LOG_PATH = REPO / "editorial" / "TRANSLATION_REVIEW_LOG.jsonl"
FULL_PATH = REPO / "editorial" / "TRANSLATION_REVIEW_INDEX.md"
PRIORITY_PATH = REPO / "editorial" / "TRANSLATION_REVIEW_PRIORITY.md"
CSV_PATH = REPO / "evidence" / "TRANSLATION_REVIEW_OCCURRENCES.csv"
JSON_PATH = REPO / "evidence" / "TRANSLATION_REVIEW_INDEX.json"


def digest(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_lf(path: pathlib.Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def clean(value: object) -> str:
    return " ".join(str(value or "").split())


def md(value: object) -> str:
    return clean(value).replace("|", r"\|")


records = [
    json.loads(line)
    for line in LOG_PATH.read_text(encoding="utf-8").splitlines()
    if line.strip()
]
metadata = records[0]
decisions = records[1:]
assert metadata["record_type"] == "metadata"
assert len(decisions) == 162
assert len({row["decision_id"] for row in decisions}) == len(decisions)


def priority(row: dict) -> str:
    if row["record_type"] == "difficult_translation_or_source_decision":
        return "P1-source-or-semantic-review"
    status = row.get("status", "")
    authorities = row.get("actual_authorities_checked", [])
    roles = {item.get("evidence_role") for item in authorities}
    decision_number = int(row["decision_id"].split("T")[1])
    if decision_number >= 79 and "provisional" in status and not (
        {"concept_usage", "lexical_semantics"} & roles
    ):
        return "P2-specialized-language-review"
    return "tracked"


def units(row: dict) -> str:
    found = []
    if row.get("unit_id"):
        found.append(row["unit_id"])
    for key in ("source_locations", "target_locations"):
        for location in row.get(key, []):
            unit_id = location.get("unit_id")
            if unit_id and unit_id not in found:
                found.append(unit_id)
    return ", ".join(found) or "ledger-level"


def choice(row: dict) -> str:
    return row.get("chosen_javanese") or row.get("chosen_wording_or_reading", "")


def question(row: dict) -> str:
    return row.get("precise_review_question", "")


def source_locations(row: dict) -> list[dict]:
    if row["record_type"] == "terminology_decision":
        return [item for item in row.get("source_locations", []) if item.get("found")]
    location = row.get("source_location")
    return [location] if location else []


def target_locations(row: dict) -> list[dict]:
    return [item for item in row.get("target_locations", []) if item.get("found", True)]


def section_for(path: str) -> str:
    normalized = path.replace("\\", "/")
    for prefix in ("translation/content/", "upstream/content/"):
        if normalized.startswith(prefix):
            normalized = normalized[len(prefix):]
    return normalized.removesuffix(".tex")


occurrences: list[dict] = []
for row in decisions:
    sources = source_locations(row)
    targets = target_locations(row)
    for index, target in enumerate(targets, 1):
        source = sources[min(index - 1, len(sources) - 1)] if sources else {}
        unit_id = (
            target.get("unit_id")
            or source.get("unit_id")
            or row.get("unit_id")
            or ""
        )
        target_path = target.get("path", "")
        source_path = source.get("path", "")
        occurrences.append(
            {
                "decision_id": row["decision_id"],
                "record_type": row["record_type"],
                "occurrence_index": index,
                "unit_id": unit_id,
                "section": section_for(target_path or source_path),
                "source_path": source_path,
                "source_line": source.get("line"),
                "target_path": target_path,
                "target_line_start": target.get("line"),
                "target_line_end": target.get("line_end", target.get("line")),
                "segment_id": target.get("segment_id", ""),
                "script": "Latn",
                "locale": "jv-Latn-ID",
                "chosen_rendering": choice(row),
                "decision_status": row.get("status", row.get("history", "")),
                "review_priority": priority(row),
                "accepted_reader_release": "",
                "accepted_pdf_page": "",
                "page_binding_status": (
                    "pending_next_accepted_reader_pagination"
                    if target_path.startswith("translation/")
                    else "not_a_reader_body_occurrence"
                ),
                "expert_question": question(row),
            }
        )

fieldnames = [
    "decision_id",
    "record_type",
    "occurrence_index",
    "unit_id",
    "section",
    "source_path",
    "source_line",
    "target_path",
    "target_line_start",
    "target_line_end",
    "segment_id",
    "script",
    "locale",
    "chosen_rendering",
    "decision_status",
    "review_priority",
    "accepted_reader_release",
    "accepted_pdf_page",
    "page_binding_status",
    "expert_question",
]
csv_buffer = io.StringIO(newline="")
writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames, lineterminator="\n")
writer.writeheader()
writer.writerows(occurrences)
CSV_PATH.write_text(csv_buffer.getvalue(), encoding="utf-8", newline="")

priority_records = [row for row in decisions if priority(row) != "tracked"]


def markdown_document(title: str, selected: list[dict], note: str) -> str:
    lines = [
        f"# {title}",
        "",
        f"Coverage: {metadata['coverage']}.",
        "",
        note,
        "",
        "Final PDF pages are intentionally blank until a later reader pagination "
        "is accepted. The published v0.1.2 reader stays sealed and predates this "
        "review projection.",
        "",
        "| ID | Priority | Type | Unit | Rendering or decision | Status | Expert double-check |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in selected:
        lines.append(
            "| "
            + " | ".join(
                [
                    md(row["decision_id"]),
                    md(priority(row)),
                    md(row["record_type"]),
                    md(units(row)),
                    md(choice(row)),
                    md(row.get("status", row.get("history", ""))),
                    md(question(row)),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "Exact source and target lines, alternatives, rationales, authorities, "
            "confidence and machine hashes remain in "
            "TRANSLATION_REVIEW_LOG.jsonl; the occurrence projection is "
            "../evidence/TRANSLATION_REVIEW_OCCURRENCES.csv.",
            "",
        ]
    )
    return "\n".join(lines)


FULL_PATH.write_text(
    markdown_document(
        "Translation decision index",
        decisions,
        "This readable index contains every current terminology, provenance and "
        "difficult translation decision. The ID links each row to the complete "
        "machine record.",
    ),
    encoding="utf-8",
)
PRIORITY_PATH.write_text(
    markdown_document(
        "Priority translation decisions for expert review",
        priority_records,
        "P1 contains every difficult semantic or source decision. P2 contains "
        "provisional specialized wording without direct concept-usage or lexical-"
        "semantics attestation. These priorities request review and do not block "
        "translation.",
    ),
    encoding="utf-8",
)

machine = {
    "schema": "jv-translation-review-index/1",
    "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "locale": "jv-Latn-ID",
    "script": "Latn",
    "coverage": metadata["coverage"],
    "source_revision": metadata["source_revision"],
    "source_log": {
        "path": "editorial/TRANSLATION_REVIEW_LOG.jsonl",
        "sha256": digest_lf(LOG_PATH),
        "hash_representation": "UTF-8 with LF-normalized line endings (Git blob)",
    },
    "pagination": {
        "status": "pending_next_accepted_reader_pagination",
        "sealed_release": "v0.1.2",
        "policy": (
            "Bind exact printed/PDF pages after the next accepted reader "
            "pagination; do not rewrite the sealed v0.1.2 lineage."
        ),
    },
    "priority_policy": {
        "P1-source-or-semantic-review": (
            "Every difficult translation or source decision."
        ),
        "P2-specialized-language-review": (
            "Current logic and proof-theory terminology (JV-T079 onward) that "
            "is provisional and lacks direct concept-usage or lexical-semantics "
            "attestation."
        ),
    },
    "counts": {
        "decisions": len(decisions),
        "terminology_decisions": sum(
            row["record_type"] == "terminology_decision" for row in decisions
        ),
        "difficult_decisions": sum(
            row["record_type"] == "difficult_translation_or_source_decision"
            for row in decisions
        ),
        "priority_decisions": len(priority_records),
        "tracked_occurrences": len(occurrences),
    },
    "priority_decision_ids": [row["decision_id"] for row in priority_records],
    "decisions": decisions,
    "occurrences": occurrences,
}
JSON_PATH.write_text(
    json.dumps(machine, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print(
    json.dumps(
        {
            "decisions": len(decisions),
            "priority_decisions": len(priority_records),
            "tracked_occurrences": len(occurrences),
            "full_index_sha256": digest(FULL_PATH),
            "priority_sha256": digest(PRIORITY_PATH),
            "csv_sha256": digest(CSV_PATH),
            "json_sha256": digest(JSON_PATH),
        }
    )
)
