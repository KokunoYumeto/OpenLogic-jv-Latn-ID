from __future__ import annotations

import csv
import datetime
import hashlib
import io
import json
import pathlib
import re

import jsonschema


REPO = pathlib.Path(__file__).resolve().parent.parent
OUT = REPO / "translation-decisions"
LOG = REPO / "editorial" / "TRANSLATION_REVIEW_LOG.jsonl"
SCHEMA = OUT / "translation-decision.schema.json"
DECISIONS = OUT / "DECISIONS.json"
FULL = OUT / "TRANSLATION_DECISIONS_FULL.md"
PRIORITY = OUT / "PRIORITY_REVIEW.md"
CSV = OUT / "DECISION_OCCURRENCES.csv"
START = OUT / "START_HERE.md"
QA = OUT / "TRANSLATION_DECISION_QA.json"
COMMIT = "b56a17886523b275a35525c106bb1932fe99e757"
SOURCE_REVISION = "9620cc73f9c8e0ad003c514a5d3748f29611c4c0"
SCHEMA_URI = (
    "https://raw.githubusercontent.com/KokunoYumeto/OpenLogic-translations/"
    "811091d54be4989918864732073279a588340e6f/catalogue/"
    "translation-decisions/translation-decision.schema.json"
)


def data(path: pathlib.Path) -> bytes:
    return path.read_bytes()


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha(path: pathlib.Path) -> str:
    return sha_bytes(data(path))


def git_blob_bytes(path: pathlib.Path) -> bytes:
    value = data(path)
    try:
        relative = path.relative_to(REPO).as_posix()
    except ValueError:
        relative = ""
    if not relative.startswith("evidence/") and path.suffix.lower() in {
        ".md",
        ".json",
        ".jsonl",
        ".csv",
        ".py",
    }:
        value = value.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return value


def public_sha(path: pathlib.Path) -> str:
    return sha_bytes(git_blob_bytes(path))


def write_lf(path: pathlib.Path, value: str) -> None:
    path.write_bytes(value.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8"))


def artifact(path_or_uri: str, path: pathlib.Path | None = None, **extra):
    record = {"path_or_uri": path_or_uri}
    if path is None:
        record["sha256"] = extra.pop("sha256")
        if "bytes" in extra:
            record["bytes"] = extra.pop("bytes")
    else:
        payload = git_blob_bytes(path)
        record.update(bytes=len(payload), sha256=sha_bytes(payload))
    record.update(extra)
    return record


def lines(path: pathlib.Path) -> list[str]:
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n").splitlines()


def line_excerpt(path: pathlib.Path, start: int, end: int) -> str:
    content = lines(path)
    start = max(1, min(start, len(content)))
    end = max(start, min(end, len(content)))
    excerpt = " ".join(line.strip() for line in content[start - 1 : end] if line.strip())
    return " ".join(excerpt.split()) or "Structural or formal locus with no prose."


def byte_span(path: pathlib.Path, start: int, end: int) -> dict[str, object]:
    raw_lines = git_blob_bytes(path).splitlines(keepends=True)
    if not raw_lines or start < 1 or end < start or end > len(raw_lines):
        return {
            "status": "pending",
            "reason": "The legacy review record has no exact resolvable line span.",
        }
    return {
        "status": "available",
        "start": sum(len(value) for value in raw_lines[: start - 1]),
        "end_exclusive": sum(len(value) for value in raw_lines[:end]),
    }


def text_locator(location: dict, side: str, fallback_term: str, fallback_sense: str):
    rel = location.get("path", "")
    file_path = REPO / rel
    start = location.get("line")
    end = location.get("line_end", start)
    if not isinstance(start, int) or not isinstance(end, int) or not file_path.is_file():
        raise ValueError(f"Unresolvable {side} locator: {location}")
    line_count = len(lines(file_path))
    start = max(1, min(start, line_count))
    end = max(start, min(end, line_count))
    actual_sha = public_sha(file_path)
    declared = location.get("raw_file_sha256")
    if declared and declared not in {sha(file_path), actual_sha}:
        raise ValueError(f"Stale file hash for {rel}: {declared} != {actual_sha}")
    return {
        "path": rel,
        "file_id": location.get("unit_id") or f"editorial:{rel}",
        "file_sha256": actual_sha,
        "line_span": {"status": "available", "start": start, "end": end},
        "byte_span": byte_span(file_path, start, end),
        "printed_page": None,
        "excerpt": location.get("matched_text") or line_excerpt(file_path, start, end),
        "term": fallback_term or None,
        "intended_sense": fallback_sense or None,
        "context": f"Exact {side} locus in the partial Javanese edition.",
    }


edition = {
    "edition_id": "openlogic-jv-Latn-ID",
    "language_tag": "jv-Latn-ID",
    "language_name": "Javanese",
    "script": "Latn",
    "territory": "Indonesia",
    "locale": "jv-Latn-ID",
    "register_or_variant": "formal written ngoko",
    "notation_profile": "international mathematical notation",
    "layer_type": "semantic_translation",
    "parent_semantic_edition_id": None,
}

records = [json.loads(value) for value in LOG.read_text(encoding="utf-8-sig").splitlines() if value.strip()]
metadata, legacy = records[0], records[1:]
assert metadata["record_type"] == "metadata"
assert len(legacy) == 177
assert len({row["decision_id"] for row in legacy}) == len(legacy)
passages = {
    row["passage_id"]: row
    for row in map(json.loads, (REPO / "evidence" / "CANON_PASSAGES.jsonl").read_text(encoding="utf-8").splitlines())
}
sources = {
    row["source_id"]: row
    for row in map(json.loads, (REPO / "evidence" / "CANON_SOURCES.jsonl").read_text(encoding="utf-8").splitlines())
}
segment_rows = [
    json.loads(value)
    for value in (REPO / "evidence" / "SEGMENT_CANON_USE.jsonl").read_text(encoding="utf-8").splitlines()
    if value.strip()
]
correction_rows = [
    json.loads(value)
    for value in (REPO / "evidence" / "SOURCE_CORRECTIONS.jsonl").read_text(encoding="utf-8").splitlines()
    if value.strip()
]
corrections_by_finding = {row["finding_id"]: row for row in correction_rows}


def record_priority(row: dict) -> str:
    if row["record_type"] == "difficult_translation_or_source_decision":
        return "high"
    status = row.get("status", "")
    roles = {item.get("evidence_role") for item in row.get("actual_authorities_checked", [])}
    number = int(row["decision_id"].split("T")[1])
    if number >= 79 and "provisional" in status and not ({"concept_usage", "lexical_semantics"} & roles):
        return "high"
    return "normal"


def confidence(row: dict) -> str:
    value = row.get("uncertainty", "").lower()
    if "high" in value:
        return "low"
    if "medium" in value:
        return "medium"
    return "high"


def recording_mode(row: dict) -> str:
    value = row.get("history", "").lower()
    if "retrospective" in value:
        return "retrospective"
    if "derived" in value:
        return "derived"
    return "contemporaneous"


def authorities(row: dict) -> list[dict]:
    result = []
    for item in row.get("actual_authorities_checked", []):
        pid = item.get("passage_id")
        if pid:
            passage = passages[pid]
            source = sources[passage["source_id"]]
            result.append(
                {
                    "authority_id": passage["source_id"],
                    "citation": f"{source['title']} ({source.get('year', 'n.d.')})",
                    "passage_id": pid,
                    "locator": f"printed page {passage.get('printed_page')}; {passage.get('region')}",
                    "source_sha256": source.get("sha256"),
                    "passage_sha256": passage["excerpt_sha256"],
                    "status": "checked_supports" if passage["evidence_role"] != "negative_technical_attestation" else "checked_adverse",
                    "note": item.get("consulted_scope") or passage["consulted_for"],
                }
            )
            continue
        authority_name = item.get("authority", "Frozen English source")
        audit_hash = item.get("review_sha256") or item.get("findings_sha256")
        result.append(
            {
                "authority_id": authority_name,
                "citation": authority_name,
                "passage_id": None,
                "locator": None,
                "source_sha256": audit_hash,
                "passage_sha256": None,
                "status": "not_checked",
                "note": item.get("role") or "Exact source/audit evidence controls this bounded mathematical reading.",
            }
        )
    if not result:
        result.append(
            {
                "authority_id": "FROZEN-OPENLOGIC-ENGLISH",
                "citation": f"OpenLogic frozen source revision {SOURCE_REVISION}",
                "passage_id": None,
                "locator": None,
                "source_sha256": None,
                "passage_sha256": None,
                "status": "not_checked",
                "note": "The frozen English source controls the mathematical sense; no specialized Javanese attestation is claimed.",
            }
        )
    return result


audit_files = {
    "OLPL-001": "evidence/OLPL001_SOURCE_AUDIT.json",
    "OLPL-002": "evidence/OLPL_TABLEAU_SOURCE_AUDIT.json",
    "OLPL-003": "evidence/OLPL_TABLEAU_SOURCE_AUDIT.json",
    "OLPL-004": "evidence/OLPL_SEQUENT_SOURCE_AUDIT.json",
    "OLPL-005": "evidence/OLPL_SEQUENT_SOURCE_AUDIT.json",
    "OLPL-006": "evidence/OLPL_SOUNDNESS_SOURCE_AUDIT.json",
    "OLPL-007": "evidence/OLPL_SOUNDNESS_SOURCE_AUDIT.json",
    "OLPL-008": "evidence/OLPL_NATURAL_DEDUCTION_SOURCE_AUDIT.json",
    "OLPL-009": "evidence/OLPL_NATURAL_DEDUCTION_SOURCE_AUDIT.json",
    "OLPL-010": "evidence/OLPL_NATURAL_DEDUCTION_SOURCE_AUDIT.json",
    "OLPL-011": "evidence/OLPL_NATURAL_DEDUCTION_SOURCE_AUDIT.json",
    "OLPL-012": "evidence/OLPL_NATURAL_DEDUCTION_SOURCE_AUDIT.json",
    "OLPL-013": "evidence/OLPL_TABLEAUX_FOUNDATIONS_SOURCE_AUDIT.json",
    "OLPL-014": "evidence/OLPL_TABLEAUX_FOUNDATIONS_SOURCE_AUDIT.json",
    "OLPL-015": "evidence/OLPL_TABLEAUX_FOUNDATIONS_SOURCE_AUDIT.json",
    "OLPL-016": "evidence/OLPL_TABLEAUX_METATHEORY_SOURCE_AUDIT.json",
    "OLPL-017": "evidence/OLPL_TABLEAUX_METATHEORY_SOURCE_AUDIT.json",
    "OLPL-018": "evidence/OLPL_TABLEAUX_METATHEORY_SOURCE_AUDIT.json",
    "OLPL-019": "evidence/OLPL_TABLEAUX_METATHEORY_SOURCE_AUDIT.json",
    "OLPL-020": "evidence/OLPL_TABLEAUX_METATHEORY_SOURCE_AUDIT.json",
    "OLPL-021": "evidence/OLPL_TABLEAUX_METATHEORY_SOURCE_AUDIT.json",
    "OLPL-022": "evidence/OLPL_TABLEAUX_METATHEORY_SOURCE_AUDIT.json",
    "OLPL-023": "evidence/OLPL_TABLEAUX_METATHEORY_SOURCE_AUDIT.json",
    "OLPL-024": "evidence/OLPL_AXIOMATIC_FOUNDATIONS_SOURCE_AUDIT.json",
    "OLPL-025": "evidence/OLPL_AXIOMATIC_FOUNDATIONS_SOURCE_AUDIT.json",
    "OLPL-026": "evidence/OLPL_AXIOMATIC_FOUNDATIONS_SOURCE_AUDIT.json",
}


def evidence_refs(row: dict) -> list[dict]:
    refs = [artifact("evidence/TERM_DECISIONS.jsonl", REPO / "evidence" / "TERM_DECISIONS.jsonl")]
    for audit_id in row.get("source_audit_ids", []):
        rel = audit_files.get(audit_id)
        if rel and artifact(rel, REPO / rel) not in refs:
            refs.append(artifact(rel, REPO / rel))
    if row["record_type"] == "difficult_translation_or_source_decision" or row.get("source_audit_ids"):
        refs.append(artifact("evidence/SOURCE_CORRECTIONS.jsonl", REPO / "evidence" / "SOURCE_CORRECTIONS.jsonl"))
    return refs


def reader_locator(target_path: str) -> dict:
    if target_path.startswith("translation/"):
        return {
            "status": "pending",
            "reason": "Bind the exact printed and assembled PDF page after a future reader pagination containing this occurrence is accepted.",
        }
    return {"status": "not_applicable", "reason": "This occurrence is editorial evidence rather than reader body text."}


def locator_from_segment(segment: dict, side: str) -> dict:
    source_side = side == "source"
    prefix = "upstream/" if source_side else "translation/"
    line_key = "source" if source_side else "translation"
    path = REPO / prefix.rstrip("/") / segment["source_path"]
    return {
        "unit_id": segment["unit_id"],
        "path": prefix + segment["source_path"],
        "line": segment[f"{line_key}_line_start"],
        "line_end": segment[f"{line_key}_line_end"],
        "segment_id": segment["segment_id"],
        "raw_file_sha256": sha(path),
    }


def segment_for_location(location: dict, side: str) -> dict | None:
    unit_id = location.get("unit_id")
    line = location.get("line")
    path = location.get("path", "").replace("\\", "/")
    for prefix in ("upstream/", "translation/"):
        if path.startswith(prefix):
            path = path[len(prefix) :]
    if not unit_id or not isinstance(line, int):
        return None
    start_key = "source_line_start" if side == "source" else "translation_line_start"
    end_key = "source_line_end" if side == "source" else "translation_line_end"
    return next(
        (
            segment
            for segment in segment_rows
            if segment["unit_id"] == unit_id
            and segment["source_path"] == path
            and segment[start_key] <= line <= segment[end_key]
        ),
        None,
    )


def visible(value: str) -> str:
    value = re.sub(r"!!(?:\^a|a|\^)?\{([^}]+)\}s?", r"\1", value)
    value = re.sub(r"\\[A-Za-z@]+", " ", value)
    value = value.replace("{", " ").replace("}", " ")
    value = re.sub(r"[^0-9A-Za-zÀ-ž]+", " ", value.lower())
    return " ".join(value.split())


def terms(value: str) -> list[str]:
    return [
        visible(item)
        for item in re.split(r"\s*;\s*|\s+/\s+|(?<!\w)/(?!\w)", value)
        if visible(item)
    ]


MANUAL_UNITS = {
    "JV-T008": ["OLP-0006"],
    "JV-T029": ["OLP-0091"],
    "JV-T038": ["OLP-0091", "OLP-0095", "OLP-0096"],
    "JV-T059": ["OLP-0042"],
    "JV-T066": ["OLP-0046"],
    "JV-T102": ["OLP-0094", "OLP-0080"],
}

MANUAL_SEGMENTS = {
    "JV-T029": [
        "OLP-0091-P007",
        "OLP-0091-P008",
        "OLP-0024-P016",
        "OLP-0048-P021",
    ],
    "JV-T038": ["OLP-0064-P007", "OLP-0091-P007", "OLP-0096-P012"],
    "JV-T066": ["OLP-0046-P010", "OLP-0046-P013"],
}


def best_segment(row: dict, source_term: str, chosen: str) -> dict:
    unit_ids = []
    for location in row.get("source_locations", []) + row.get("target_locations", []):
        if location.get("unit_id"):
            unit_ids.append(location["unit_id"])
        unit_ids.extend(location.get("searched_units", []))
    unit_ids.extend(MANUAL_UNITS.get(row["decision_id"], []))
    if row.get("unit_id"):
        unit_ids.append(row["unit_id"])
    unit_ids = list(dict.fromkeys(unit_ids))
    source_terms = terms(source_term)
    target_terms = terms(chosen)
    candidates = []
    for segment in segment_rows:
        if segment["classification"] != "translated" or segment["unit_id"] not in unit_ids:
            continue
        source_text = visible(
            line_excerpt(
                REPO / "upstream" / segment["source_path"],
                segment["source_line_start"],
                segment["source_line_end"],
            )
        )
        target_text = visible(
            line_excerpt(
                REPO / "translation" / segment["source_path"],
                segment["translation_line_start"],
                segment["translation_line_end"],
            )
        )
        score = sum(term in source_text for term in source_terms) + sum(
            term in target_text for term in target_terms
        )
        candidates.append((score, -len(source_text) - len(target_text), segment, source_text, target_text))
    if not candidates:
        raise ValueError(f"Decision {row['decision_id']} has no translated segment in its unit hints")
    score, _, segment, source_text, target_text = max(candidates, key=lambda item: (item[0], item[1]))
    if score == 0 and row["decision_id"] not in MANUAL_UNITS:
        raise ValueError(
            f"Decision {row['decision_id']} has no term-bearing fallback segment; "
            f"units={unit_ids!r}; source_terms={source_terms!r}; target_terms={target_terms!r}; "
            f"best={segment['segment_id']} source={source_text!r} target={target_text!r}"
        )
    return segment


def correction_occurrences(row: dict, source_term: str, intended_sense: str) -> list[dict]:
    result = []
    for index, finding_id in enumerate(row.get("source_audit_ids", []), 1):
        correction = corrections_by_finding.get(finding_id)
        if not correction:
            continue
        source_record = correction["source"]
        target_record = correction["target"]
        numbers = [int(value) for value in re.findall(r"\d+", source_record["locator"])]
        source_start = numbers[0]
        source_end = numbers[-1]
        context = target_record.get("adjacent_contexts", [{}])[0]
        target_start = context.get("line_start") or target_record["adjacent_note_lines"][0]
        target_end = context.get("line_end") or target_start
        source_location = {
            "unit_id": source_record["unit_id"],
            "path": "upstream/" + source_record["path"],
            "line": source_start,
            "line_end": source_end,
            "raw_file_sha256": source_record["sha256"],
        }
        target_location = {
            "unit_id": source_record["unit_id"],
            "path": target_record["path"],
            "line": target_start,
            "line_end": target_end,
            "raw_file_sha256": target_record["sha256"],
        }
        segment = segment_for_location(target_location, "target")
        semantic_unit_id = (
            segment["segment_id"]
            if segment
            else f"{source_record['unit_id']}:source-correction-{finding_id}"
        )
        result.append(
            {
                "occurrence_id": f"jv-Latn-ID-{row['decision_id']}-OCC-{index:03d}",
                "unit_id": source_record["unit_id"],
                "semantic_unit_id": semantic_unit_id,
                "part_title": None,
                "chapter_title": None,
                "section_title": target_record["path"].removesuffix(".tex"),
                "source": text_locator(source_location, "source", source_term, intended_sense),
                "target": text_locator(target_location, "target", row.get("chosen_javanese", ""), intended_sense),
                "reader_locator": reader_locator(target_record["path"]),
                "evidence_refs": evidence_refs(row),
            }
        )
    return result


def paired_occurrences(row: dict, source_term: str, intended_sense: str) -> list[dict]:
    chosen = row.get("chosen_javanese") or row.get("chosen_wording_or_reading", "")
    if row["record_type"] == "terminology_decision" and row.get("source_audit_ids"):
        corrected = correction_occurrences(row, source_term, intended_sense)
        if corrected:
            return corrected
    if row["record_type"] == "terminology_decision":
        source_locations = [item for item in row.get("source_locations", []) if item.get("found")]
    else:
        source_locations = [row["source_location"]] if row.get("source_location", {}).get("line") else []
    target_locations = [item for item in row.get("target_locations", []) if item.get("found", True) and item.get("line")]
    pairs: list[tuple[dict, dict, dict | None]] = []
    if target_locations:
        for target in target_locations:
            segment = segment_for_location(target, "target")
            source = locator_from_segment(segment, "source") if segment else source_locations[0]
            pairs.append((source, target, segment))
    elif source_locations:
        for source in source_locations:
            segment = segment_for_location(source, "source")
            if not segment:
                raise ValueError(f"Decision {row['decision_id']} source locus has no aligned segment")
            pairs.append((source, locator_from_segment(segment, "target"), segment))
    elif row["decision_id"] in MANUAL_SEGMENTS:
        for segment_id in MANUAL_SEGMENTS[row["decision_id"]]:
            segment = next(
                (item for item in segment_rows if item["segment_id"] == segment_id),
                None,
            )
            if not segment or segment["classification"] != "translated":
                raise ValueError(
                    f"Decision {row['decision_id']} has an unavailable manual segment {segment_id}"
                )
            pairs.append(
                (
                    locator_from_segment(segment, "source"),
                    locator_from_segment(segment, "target"),
                    segment,
                )
            )
    else:
        segment = best_segment(row, source_term, chosen)
        pairs.append((locator_from_segment(segment, "source"), locator_from_segment(segment, "target"), segment))
    result = []
    for index, (source, target, segment) in enumerate(pairs, 1):
        unit_id = target.get("unit_id") or source.get("unit_id") or row.get("unit_id")
        if not unit_id:
            raise ValueError(f"Decision {row['decision_id']} occurrence lacks unit ID")
        semantic_unit_id = (segment or {}).get("segment_id") or target.get("segment_id") or f"{unit_id}:review-{row['decision_id']}-{index:03d}"
        result.append(
            {
                "occurrence_id": f"jv-Latn-ID-{row['decision_id']}-OCC-{index:03d}",
                "unit_id": unit_id,
                "semantic_unit_id": semantic_unit_id,
                "part_title": None,
                "chapter_title": None,
                "section_title": target.get("path", "").removesuffix(".tex"),
                "source": text_locator(source, "source", source_term, intended_sense),
                "target": text_locator(target, "target", chosen, intended_sense),
                "reader_locator": reader_locator(target.get("path", "")),
                "evidence_refs": evidence_refs(row),
            }
        )
    return result


decisions = []
for row in legacy:
    terminology = row["record_type"] == "terminology_decision"
    source_term = row.get("english_term_or_issue") or row.get("issue")
    chosen = row.get("chosen_javanese") or row.get("chosen_wording_or_reading")
    intended = row.get("chosen_sense_and_constraints") or row.get("issue")
    rationale = row.get("chosen_sense_and_constraints") or (
        f"The frozen English formulas, definitions and finite checks establish this reading. {row.get('javanese_canon_status', '')}"
    )
    alternatives = [
        {
            "rendering": value,
            "disposition": "viable_alternative" if terminology else "rejected",
            "reason": "Listed for expert comparison; the current rendering remains reversible." if terminology else "Rejected because it would retain or conceal the identified source defect.",
        }
        for value in row.get("alternatives_for_review", [])
        if value.strip()
    ]
    conf = confidence(row)
    provisional = "provisional" in row.get("status", "") or conf != "high" or row.get("open_to_correction", False)
    question = row.get("precise_review_question")
    priority = record_priority(row)
    decisions.append(
        {
            "decision_id": row["decision_id"],
            "supersedes": [],
            "record_kind": (
                "source_correction"
                if (not terminology or row.get("source_audit_ids"))
                else "terminology"
            ),
            "recording_mode": recording_mode(row),
            "recorded_utc": metadata["generated_utc"],
            "edition": edition,
            "source_term_or_construction": source_term,
            "intended_sense": intended,
            "chosen_rendering": chosen,
            "rationale": rationale,
            "authorities_checked": authorities(row),
            "alternatives": alternatives,
            "confidence": conf,
            "confidence_reason": row.get("uncertainty", "Evidence strength is stated in the legacy decision record."),
            "provisional": provisional,
            "review_priority": priority,
            "expert_review_useful": priority in {"urgent", "high"} or provisional,
            "expert_review_reason": row.get("not_found_or_scope_limit") or row.get("javanese_canon_status"),
            "please_double_check_question": question,
            "occurrences": paired_occurrences(row, source_term, intended),
        }
    )

machine = {
    "schema_version": "openlogic-translation-decisions/1.0.0",
    "edition_release": {
        "edition": edition,
        "release_tag": None,
        "repository": "https://github.com/KokunoYumeto/OpenLogic-jv-Latn-ID",
        "doi": None,
        "source_revision": SOURCE_REVISION,
        "coverage_state": "partial",
        "source_units": 118,
        "reader_units": 24,
    },
    "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "generator": artifact("tools/build-translation-decisions.py", pathlib.Path(__file__)),
    "decisions": decisions,
}

schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
jsonschema.Draft202012Validator.check_schema(schema)
validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
errors = sorted(validator.iter_errors(machine), key=lambda error: list(error.absolute_path))
if errors:
    raise ValueError("\n".join(f"{list(error.absolute_path)}: {error.message}" for error in errors[:20]))

write_lf(DECISIONS, json.dumps(machine, ensure_ascii=False, indent=2) + "\n")


def clean(value: object) -> str:
    return " ".join(str(value or "").split())


def md(value: object) -> str:
    return clean(value).replace("|", r"\|")


def markdown(title: str, selected: list[dict], intro: str) -> str:
    values = [
        f"# {title}",
        "",
        intro,
        "",
        "Coverage: OLP-0001 through OLP-0118; 118 of 722 frozen source units. Reader-page bindings remain pending until a future pagination containing each occurrence is accepted.",
        "",
        "| ID | Priority | Kind | Source | Chosen rendering | Confidence | Expert question |",
        "|---|---|---|---|---|---|---|",
    ]
    for decision in selected:
        values.append(
            "| "
            + " | ".join(
                [
                    md(decision["decision_id"]),
                    md(decision["review_priority"]),
                    md(decision["record_kind"]),
                    md(decision["source_term_or_construction"]),
                    md(decision["chosen_rendering"]),
                    md(decision["confidence"]),
                    md(decision["please_double_check_question"]),
                ]
            )
            + " |"
        )
    values.extend(["", "Exact hashes, spans, authorities, alternatives and occurrences are in `DECISIONS.json`.", ""])
    return "\n".join(values)


write_lf(
    FULL,
    markdown(
        "Full translation decision register",
        decisions,
        "Every current terminology and difficult source/translation decision is listed here for human review.",
    ),
)
priority_decisions = [decision for decision in decisions if decision["review_priority"] in {"urgent", "high"}]
write_lf(
    PRIORITY,
    markdown(
        "Priority review",
        priority_decisions,
        "These decisions most benefit from expert attention. Review is useful but does not block the source-faithful translation lane.",
    ),
)

fieldnames = [
    "occurrence_id",
    "decision_id",
    "unit_id",
    "semantic_unit_id",
    "source_path",
    "source_line_start",
    "source_line_end",
    "source_sha256",
    "target_path",
    "target_line_start",
    "target_line_end",
    "target_sha256",
    "reader_status",
    "printed_page",
    "assembled_pdf_page",
]
rows = []
for decision in decisions:
    for occurrence in decision["occurrences"]:
        rows.append(
            {
                "occurrence_id": occurrence["occurrence_id"],
                "decision_id": decision["decision_id"],
                "unit_id": occurrence["unit_id"],
                "semantic_unit_id": occurrence["semantic_unit_id"],
                "source_path": occurrence["source"]["path"],
                "source_line_start": occurrence["source"]["line_span"].get("start", ""),
                "source_line_end": occurrence["source"]["line_span"].get("end", ""),
                "source_sha256": occurrence["source"]["file_sha256"],
                "target_path": occurrence["target"]["path"],
                "target_line_start": occurrence["target"]["line_span"].get("start", ""),
                "target_line_end": occurrence["target"]["line_span"].get("end", ""),
                "target_sha256": occurrence["target"]["file_sha256"],
                "reader_status": occurrence["reader_locator"]["status"],
                "printed_page": occurrence["reader_locator"].get("printed_page", ""),
                "assembled_pdf_page": occurrence["reader_locator"].get("assembled_pdf_page", ""),
            }
        )
csv_buffer = io.StringIO(newline="")
writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames, lineterminator="\n")
writer.writeheader()
writer.writerows(rows)
write_lf(CSV, csv_buffer.getvalue())

write_lf(
    START,
    """# Translation decisions: start here

This directory exposes the canonical OpenLogic translation-decision contract for the partial Javanese Latin edition.

- `TRANSLATION_DECISIONS_FULL.md` is the complete readable index.
- `PRIORITY_REVIEW.md` is the focused expert-review queue.
- `DECISION_OCCURRENCES.csv` has one row per exact source-target locus.
- `DECISIONS.json` is the normative edition data validated against `translation-decision.schema.json`.
- `TRANSLATION_DECISION_QA.json` records deterministic validation and projection agreement.

The edition is a formal written ngoko semantic translation in Latin script for Javanese readers in Indonesia. International mathematical notation remains unchanged. A deterministic Javanese-script projection may be useful as a separately tested companion, but the present evidence does not justify claiming a second independently translated semantic edition or splitting regional/register variants. Reader pages stay explicitly pending until a future accepted pagination contains the corresponding occurrence. The published v0.1.2 reader remains sealed.
""",
)

decision_ids = [decision["decision_id"] for decision in decisions]
occurrences = [
    occurrence
    for decision in decisions
    for occurrence in decision["occurrences"]
]
occurrence_ids = [occurrence["occurrence_id"] for occurrence in occurrences]
assert len(decision_ids) == len(set(decision_ids))
assert len(occurrence_ids) == len(set(occurrence_ids))
for occurrence in occurrences:
    for side in ("source", "target"):
        locator = occurrence[side]
        file_path = REPO / locator["path"]
        assert file_path.is_file(), locator["path"]
        payload = git_blob_bytes(file_path)
        assert locator["file_sha256"] == sha_bytes(payload), locator["path"]
        line_span = locator["line_span"]
        span = locator["byte_span"]
        assert line_span["status"] == span["status"] == "available"
        raw_lines = payload.splitlines(keepends=True)
        start = line_span["start"]
        end = line_span["end"]
        assert 1 <= start <= end <= len(raw_lines)
        assert span["start"] == sum(len(value) for value in raw_lines[: start - 1])
        assert span["end_exclusive"] == sum(len(value) for value in raw_lines[:end])
        assert span["start"] < span["end_exclusive"] <= len(payload)
    reader = occurrence["reader_locator"]
    assert reader["status"] in {"pending", "not_applicable"}
    assert "printed_page" not in reader and "assembled_pdf_page" not in reader

parsed_csv = list(csv.DictReader(io.StringIO(CSV.read_text(encoding="utf-8"))))
assert len(parsed_csv) == len(rows) == len(occurrences)
assert {row["occurrence_id"] for row in parsed_csv} == set(occurrence_ids)
assert sum(line.startswith("| JV-") for line in FULL.read_text(encoding="utf-8").splitlines()) == len(decisions)
assert sum(line.startswith("| JV-") for line in PRIORITY.read_text(encoding="utf-8").splitlines()) == len(priority_decisions)
assert len(json.loads(DECISIONS.read_text(encoding="utf-8"))["decisions"]) == len(decisions)

qa = {
    "schema": "openlogic-translation-decision-qa/1.0.0",
    "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "status": "PASS",
    "normative_schema": {
        "path": "translation-decision.schema.json",
        "canonical_uri": SCHEMA_URI,
        "bytes": SCHEMA.stat().st_size,
        "sha256": sha(SCHEMA),
        "expected_sha256": "50e7fa407b62c711f92f8b93be591d3b4a6e1c4adb1386c398bb5f76844d9f90",
        "draft": "2020-12",
        "schema_validation": "PASS",
    },
    "edition": {"language_tag": "jv-Latn-ID", "script": "Latn", "coverage": "partial-118/722"},
    "counts": {
        "decisions": len(decisions),
        "terminology": sum(value["record_kind"] == "terminology" for value in decisions),
        "source_corrections": sum(value["record_kind"] == "source_correction" for value in decisions),
        "priority": len(priority_decisions),
        "occurrences": len(rows),
        "unique_decision_ids": len({value["decision_id"] for value in decisions}),
        "unique_occurrence_ids": len({row["occurrence_id"] for row in rows}),
    },
    "checks": {
        "schema_instance": "PASS",
        "unique_decision_ids": "PASS",
        "unique_occurrence_ids": "PASS",
        "source_target_paths_exist": "PASS",
        "source_target_hashes_match": "PASS",
        "line_and_byte_spans_resolve": "PASS",
        "reader_pages_never_guessed": "PASS",
        "markdown_csv_json_counts_agree": "PASS",
    },
    "provenance": {
        "source_revision": SOURCE_REVISION,
        "public_checkpoint_commit": COMMIT,
        "legacy_review_log": artifact("editorial/TRANSLATION_REVIEW_LOG.jsonl", LOG),
        "term_ledger": artifact("evidence/TERM_DECISIONS.jsonl", REPO / "evidence" / "TERM_DECISIONS.jsonl"),
        "batch_qa": artifact("evidence/BATCH_QA.json", REPO / "evidence" / "BATCH_QA.json"),
    },
    "generated_artifacts": [],
}
write_lf(QA, json.dumps(qa, ensure_ascii=False, indent=2) + "\n")
qa["generated_artifacts"] = [
    artifact(path.name, path)
    for path in (START, FULL, PRIORITY, CSV, DECISIONS, SCHEMA)
]
write_lf(QA, json.dumps(qa, ensure_ascii=False, indent=2) + "\n")

print(
    json.dumps(
        {
            "status": "PASS",
            "decisions": len(decisions),
            "priority": len(priority_decisions),
            "occurrences": len(rows),
            "decisions_sha256": sha(DECISIONS),
            "qa_sha256": sha(QA),
        }
    )
)
