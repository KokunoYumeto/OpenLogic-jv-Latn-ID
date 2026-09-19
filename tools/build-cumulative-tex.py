#!/usr/bin/env python3
"""Assemble the released modular reader into one directly editable TeX file."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess


READER_BODY_PATHS = [
    "translation/content/open-logic-about.tex",
    "translation/content/sets-functions-relations/sets/sets.tex",
    "translation/content/sets-functions-relations/sets/basics.tex",
    "translation/content/sets-functions-relations/sets/subsets.tex",
    "translation/content/sets-functions-relations/sets/important-sets.tex",
    "translation/content/sets-functions-relations/sets/unions-and-intersections.tex",
    "translation/content/sets-functions-relations/sets/pairs-and-products.tex",
    "translation/content/sets-functions-relations/sets/russells-paradox.tex",
    "translation/content/sets-functions-relations/relations/relations-complete.tex",
    "translation/content/sets-functions-relations/relations/relations-as-sets.tex",
    "translation/content/sets-functions-relations/relations/reflections.tex",
    "translation/content/sets-functions-relations/relations/special-properties.tex",
    "translation/content/sets-functions-relations/relations/equivalence-relations.tex",
    "translation/content/sets-functions-relations/relations/orders.tex",
    "translation/content/sets-functions-relations/relations/graphs.tex",
    "translation/content/sets-functions-relations/relations/trees.tex",
    "translation/content/sets-functions-relations/relations/operations.tex",
    "translation/content/sets-functions-relations/functions/functions.tex",
    "translation/content/sets-functions-relations/functions/function-basics.tex",
    "translation/content/sets-functions-relations/functions/function-kinds.tex",
    "translation/content/sets-functions-relations/functions/functions-relations.tex",
    "translation/content/sets-functions-relations/functions/inverses.tex",
    "translation/content/sets-functions-relations/functions/composition.tex",
    "translation/content/sets-functions-relations/functions/partial-functions.tex",
]
DOCUMENT_WRAPPER = re.compile(
    r"(?m)^\s*\\documentclass(?:\[[^\]]*\])?\{subfiles\}\s*$|"
    r"^\s*\\begin\{document\}\s*$|^\s*\\end\{document\}\s*$"
)
OLIMPORT = re.compile(
    r"(?m)^(?P<indent>[ \t]*)\\olimport"
    r"(?P<star>\*)?(?:\[(?P<directory>[^\]]+)\])?"
    r"\{(?P<name>[^}]+)\}(?:\[(?P<section>[^\]]+)\])?[ \t]*$"
)
INPUT = re.compile(r"(?m)^(?P<indent>[ \t]*)\\input\{(?P<path>[^}]+)\}[ \t]*$")


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def normalize(path: Path) -> Path:
    return path.resolve()


def repo_relative(repo: Path, path: Path) -> str:
    return normalize(path).relative_to(normalize(repo)).as_posix()


class Assembler:
    def __init__(self, repo: Path):
        self.repo = normalize(repo)
        self.edition = self.repo / "edition"
        self.body_files: list[str] = []
        self.dependencies: list[str] = []

    def read(self, path: Path) -> str:
        return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")

    def expand_body(self, path: Path) -> str:
        path = normalize(path)
        relative = repo_relative(self.repo, path)
        if relative in self.body_files:
            raise ValueError(f"Reader body imported twice: {relative}")
        self.body_files.append(relative)
        source = DOCUMENT_WRAPPER.sub("", self.read(path))
        source = self.expand_imports(source, path.parent)
        base = os.path.relpath(path.parent, self.edition).replace(os.sep, "/") + "/"
        return (
            f"% >>> BEGIN INCLUDED FILE: {relative}\n"
            "\\begingroup\n"
            f"\\def\\olfilename{{{path.stem}}}\n"
            f"\\def\\olfilebase{{{base}}}\n"
            f"{source.strip()}\n"
            "\\endgroup\n"
            f"% <<< END INCLUDED FILE: {relative}"
        )

    def expand_imports(self, source: str, current_directory: Path) -> str:
        def replace_import(match: re.Match[str]) -> str:
            if match.group("star"):
                raise ValueError("Starred olimport is not supported in the bounded reader")
            directory = match.group("directory")
            base = current_directory / directory if directory else current_directory
            imported = normalize(base / (match.group("name") + ".tex"))
            return self.expand_body(imported)

        return OLIMPORT.sub(replace_import, source)

    def assemble(self, master: Path) -> str:
        master = normalize(master)
        source = self.read(master)

        def replace_input(match: re.Match[str]) -> str:
            raw = match.group("path")
            if raw.startswith(r"\olpath/"):
                candidate = normalize(self.repo / "upstream" / raw.removeprefix(r"\olpath/"))
            else:
                suffix = Path(raw).suffix
                candidate = normalize(master.parent / (raw if suffix else raw + ".tex"))
            relative = repo_relative(self.repo, candidate)
            if relative.startswith("translation/content/"):
                return self.expand_body(candidate)
            if relative == "edition/jv-errata.tex":
                self.dependencies.append(relative)
                return (
                    f"% >>> BEGIN INCLUDED FILE: {relative}\n"
                    f"{self.read(candidate).strip()}\n"
                    f"% <<< END INCLUDED FILE: {relative}"
                )
            self.dependencies.append(relative)
            return match.group(0)

        source = INPUT.sub(replace_input, source)
        source = self.expand_imports(source, master.parent)
        if self.body_files != READER_BODY_PATHS:
            raise ValueError(
                "Reader import order differs from the declared 24-unit scope:\n"
                + json.dumps(self.body_files, ensure_ascii=False, indent=2)
            )
        return source.strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    parser.add_argument("--master", default="edition/jv-sets.tex")
    parser.add_argument("--output", required=True)
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--commit")
    args = parser.parse_args()

    repo = normalize(Path(args.repo))
    commit = args.commit or subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=repo, text=True
    ).strip()
    resolved = subprocess.check_output(
        ["git", "rev-parse", f"{commit}^{{commit}}"], cwd=repo, text=True
    ).strip()
    if resolved != commit:
        raise ValueError(f"Commit must be a full exact commit id: {commit} != {resolved}")

    assembler = Assembler(repo)
    assembled = assembler.assemble(repo / args.master)
    bound_paths = [args.master, "edition/jv-errata.tex", *assembler.body_files]
    clean = subprocess.run(
        ["git", "diff", "--quiet", commit, "--", *bound_paths], cwd=repo
    ).returncode
    if clean != 0:
        raise ValueError("Cumulative TeX inputs differ from the declared source commit")
    header = (
        "% OpenLogic Javanese cumulative reader source\n"
        "% Generated deterministically from the modular tagged source tree.\n"
        f"% Source commit: {commit}\n"
        "% Put this file in edition/ inside the accompanying full-source ZIP to build it.\n"
        "% The ZIP preserves the authoritative modular structure and all dependencies.\n\n"
    )
    output = normalize(Path(args.output))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes((header + assembled).encode("utf-8"))
    if OLIMPORT.search(output.read_text(encoding="utf-8")):
        raise ValueError("Unexpanded reader import remains in cumulative TeX")

    body_records = []
    for relative in assembler.body_files:
        payload = (repo / relative).read_bytes()
        body_records.append({"path": relative, "bytes": len(payload), "sha256": sha256(payload)})
    receipt = {
        "schema": "openlogic-jv-cumulative-tex/1",
        "status": "PASS",
        "source_commit": commit,
        "master": args.master,
        "reader_body_units": 24,
        "reader_body_files": body_records,
        "inlined_editorial_files": ["edition/jv-errata.tex"],
        "retained_dependencies": sorted(set(assembler.dependencies)),
        "output": {
            "filename": output.name,
            "bytes": output.stat().st_size,
            "sha256": sha256(output.read_bytes()),
        },
    }
    receipt_path = normalize(Path(args.receipt))
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
