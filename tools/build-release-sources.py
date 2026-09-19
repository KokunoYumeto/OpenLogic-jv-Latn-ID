#!/usr/bin/env python3
"""Create and verify a deterministic full editable-source archive for a release."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile


PROTECTED_UNPUBLISHED = [
    "evidence/OLPL_AXIOMATIC_COMPLETION_SOURCE_AUDIT.json",
    "translation/content/first-order-logic/axiomatic-deduction/deduction-theorem-quantifiers.tex",
    "translation/content/first-order-logic/axiomatic-deduction/deduction-theorem.tex",
    "translation/content/first-order-logic/axiomatic-deduction/identity.tex",
    "translation/content/first-order-logic/axiomatic-deduction/provability-consistency.tex",
    "translation/content/first-order-logic/axiomatic-deduction/provability-propositional.tex",
    "translation/content/first-order-logic/axiomatic-deduction/provability-quantifiers.tex",
    "translation/content/first-order-logic/axiomatic-deduction/soundness.tex",
]
REQUIRED = [
    "BUILD.md",
    "LICENSE.md",
    "README.md",
    "edition/jv-sets.tex",
    "edition/jv-localization.sty",
    "edition/jv-errata.tex",
    "tools/build-reader.ps1",
    "tools/build-cumulative-tex.py",
    "tools/build-release-sources.py",
    "tools/build-epub.py",
    "tools/audit-epub.py",
    "tools/accept-epub-runtime.mjs",
    "upstream/assets/diagrams/bijective.tikz",
    "upstream/assets/diagrams/composition.tikz",
    "upstream/assets/diagrams/difference.tikz",
    "upstream/assets/diagrams/function.tikz",
    "upstream/assets/diagrams/injective.tikz",
    "upstream/assets/diagrams/intersection.tikz",
    "upstream/assets/diagrams/surjective.tikz",
    "upstream/assets/diagrams/union.tikz",
    "upstream/sty/open-logic.sty",
    "upstream/bib/open-logic.bib",
    "upstream/bib/natbib-oup.bst",
    "upstream/include/open-logic-chapter.tex",
    "upstream/include/open-logic-part.tex",
    "upstream/include/open-logic-section.tex",
]


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def run(repo: Path, *args: str) -> str:
    return subprocess.check_output(args, cwd=repo, text=True).strip()


def git_tree(repo: Path, commit: str) -> list[dict[str, object]]:
    raw = subprocess.check_output(
        ["git", "ls-tree", "-r", "-z", commit], cwd=repo
    )
    metadata: list[tuple[str, str, str]] = []
    for record in raw.rstrip(b"\0").split(b"\0"):
        header, path_raw = record.split(b"\t", 1)
        mode, object_type, object_id = header.decode("ascii").split()
        if object_type != "blob":
            raise ValueError(f"Non-blob Git tree entry is not supported: {path_raw!r}")
        metadata.append((mode, object_id, path_raw.decode("utf-8")))

    cat = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=repo,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    output, _ = cat.communicate(
        "".join(object_id + "\n" for _, object_id, _ in metadata).encode("ascii")
    )
    if cat.returncode != 0:
        raise subprocess.CalledProcessError(cat.returncode, cat.args)
    stream = memoryview(output)
    offset = 0
    entries: list[dict[str, object]] = []
    for mode, expected_id, path in metadata:
        line_end = output.index(b"\n", offset)
        object_id, object_type, size_raw = output[offset:line_end].decode("ascii").split()
        size = int(size_raw)
        offset = line_end + 1
        payload = bytes(stream[offset : offset + size])
        offset += size
        if output[offset : offset + 1] != b"\n":
            raise ValueError(f"Malformed git cat-file stream after {path}")
        offset += 1
        if object_id != expected_id or object_type != "blob":
            raise ValueError(f"Git object mismatch for {path}")
        entries.append(
            {"mode": mode, "object_id": object_id, "path": path, "payload": payload}
        )
    if offset != len(output):
        raise ValueError("Trailing data in git cat-file stream")
    return entries


def build_archive(entries: list[dict[str, object]], prefix: str, output: Path) -> None:
    with zipfile.ZipFile(output, "w") as archive:
        for entry in entries:
            info = zipfile.ZipInfo(
                f"{prefix}/{entry['path']}", date_time=(1980, 1, 1, 0, 0, 0)
            )
            info.create_system = 3
            info.external_attr = int(str(entry["mode"]), 8) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(
                info,
                entry["payload"],
                compress_type=zipfile.ZIP_DEFLATED,
                compresslevel=9,
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    parser.add_argument("--commit", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    commit = run(repo, "git", "rev-parse", f"{args.commit}^{{commit}}")
    if commit != args.commit:
        raise ValueError(f"Commit must be a full exact commit id: {args.commit} != {commit}")
    prefix = f"OpenLogic-jv-Latn-ID-{args.version}"
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    entries = git_tree(repo, commit)
    build_archive(entries, prefix, output)
    with tempfile.TemporaryDirectory(prefix="jv-source-replay-") as directory:
        replay = Path(directory) / output.name
        build_archive(entries, prefix, replay)
        cold_identical = output.read_bytes() == replay.read_bytes()
    if not cold_identical:
        raise ValueError("Cold git-archive replay is not byte-identical")

    tracked = [str(entry["path"]) for entry in entries]
    payload_by_path = {str(entry["path"]): entry["payload"] for entry in entries}
    expected = {f"{prefix}/{path}" for path in tracked}
    with zipfile.ZipFile(output) as archive:
        bad_member = archive.testzip()
        names = {name for name in archive.namelist() if not name.endswith("/")}
        if bad_member is not None:
            raise ValueError(f"Corrupt ZIP member: {bad_member}")
        if names != expected:
            raise ValueError(
                f"ZIP tree differs from Git tree: missing={sorted(expected - names)[:10]}, "
                f"extra={sorted(names - expected)[:10]}"
            )
        byte_mismatches = [
            path
            for path, payload in payload_by_path.items()
            if archive.read(f"{prefix}/{path}") != payload
        ]
        if byte_mismatches:
            raise ValueError(f"ZIP members differ from Git blob bytes: {byte_mismatches[:10]}")
        required_missing = [path for path in REQUIRED if f"{prefix}/{path}" not in names]
        protected_present = [path for path in PROTECTED_UNPUBLISHED if f"{prefix}/{path}" in names]
        if required_missing:
            raise ValueError(f"Required editable-source inputs missing: {required_missing}")
        if protected_present:
            raise ValueError(f"Protected unpublished files entered archive: {protected_present}")
        batch = json.loads(archive.read(f"{prefix}/evidence/BATCH_QA.json"))
        if batch["checked_units"] != 118 or batch["failures"] != 0:
            raise ValueError("Archive does not carry the accepted 118-unit zero-failure snapshot")
        missing_bodies = [
            row["source_path"]
            for row in batch["units"]
            if f"{prefix}/translation/{row['source_path']}" not in names
        ]
        if missing_bodies:
            raise ValueError(f"Translated bodies missing from archive: {missing_bodies[:10]}")

    receipt = {
        "schema": "openlogic-jv-full-source-archive/1",
        "status": "PASS",
        "version": args.version,
        "source_commit": commit,
        "archive": {
            "filename": output.name,
            "bytes": output.stat().st_size,
            "sha256": sha256(output.read_bytes()),
            "entries": len(expected),
            "prefix": prefix + "/",
        },
        "scope": {
            "translated_source_units": batch["checked_units"],
            "total_source_units": batch["total_units"],
            "reader_body_units": 24,
        },
        "verification": {
            "archive_test": "PASS",
            "exact_git_tree": True,
            "exact_git_blob_bytes": True,
            "cold_build_identical": cold_identical,
            "required_master_styles_macros_bibliography_and_scripts_present": True,
            "all_accepted_translation_bodies_present": True,
            "protected_unpublished_files_absent": True,
        },
        "required_paths": REQUIRED,
    }
    receipt_path = Path(args.receipt).resolve()
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
