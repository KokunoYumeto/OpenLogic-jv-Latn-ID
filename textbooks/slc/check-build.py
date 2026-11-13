"""Check the actual TeX import, summary, and glossary inventories."""

import argparse
import json
from pathlib import Path
import re


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("book", type=Path)
    parser.add_argument("--cumulative", action="store_true")
    args = parser.parse_args()
    project = Path(__file__).resolve().parent
    book = args.book.resolve()
    locale = book.parent.parent
    job = "slc-screen-jv" if args.cumulative else "slc-screen"
    manifest = json.loads((project / "MANIFEST.json").read_bytes())["screen"]
    scope = (project / "locale/scope.txt").read_text(encoding="utf-8").splitlines()
    content = locale / "content"
    paths = [
        (book / line[6:]).resolve()
        for line in (book / f"{job}.fls").read_text(encoding="utf-8").splitlines()
        if line.startswith("INPUT ")
    ]
    imports = {
        path.relative_to(locale).as_posix()
        for path in paths
        if path.is_relative_to(content) and path.suffix == ".tex"
    }
    expected = set(scope)
    if args.cumulative:
        if imports:
            raise SystemExit("Cumulative mode read modular content files.")
        embedded = {path.name for path in paths if re.fullmatch(r"slc-module-\d{3}\.tex", path.name)}
        expected = {f"slc-module-{index:03d}.tex" for index in range(1, len(scope) + 1)}
        imports = embedded
    if imports != expected:
        missing = sorted(expected - imports)
        extra = sorted(imports - expected)
        raise SystemExit(f"Textbook import mismatch. Missing {missing}, extra {extra}")

    gloss = "slc-embedded-glossary.tex" if args.cumulative else "include/glossary.tex"
    glossary = (book / gloss).read_text(encoding="utf-8")
    sort_keys = dict(re.findall(r"(?m)^\\slcterm(?:\[.*?\])?\{([^}]+)\}\{([^}]+)\}", glossary))
    gls = (book / f"{job}.gls").read_text(encoding="utf-8")
    rendered = re.findall(r"(?m)^\\glossentry\{([^}]+)\}", gls)
    if len(rendered) != manifest["glossary_entries"] or set(rendered) != set(sort_keys):
        raise SystemExit("The built glossary does not have the full entry inventory.")
    order = [sort_keys[key] for key in rendered]
    if order != sorted(order):
        raise SystemExit("The built glossary is out of order.")

    summary_pattern = r"slc-embedded-summary-(\d+)\.tex" if args.cumulative else r"summary-(\d+)\.tex"
    summaries = {int(match[1]) for path in paths if (match := re.fullmatch(summary_pattern, path.name))}
    if summaries != set(manifest["chapter_summaries"]):
        raise SystemExit(f"Summary import mismatch. Observed {sorted(summaries)}.")
    print(json.dumps({
        "imported_modules": len(imports), "glossary_entries": len(rendered),
        "glossary_sorted": True, "chapter_summaries": sorted(summaries),
    }))


if __name__ == "__main__":
    main()
