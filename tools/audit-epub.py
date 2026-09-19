#!/usr/bin/env python3
"""Independent structural, source-coverage, math, and link audit for the Javanese EPUB."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import html
import json
from pathlib import Path, PurePosixPath
import re
import sys
import zipfile
from xml.etree import ElementTree as ET


LANGUAGE = "jv-Latn-ID"
TITLE = "OpenLogic: Himpunan, Relasi, lan Fungsi"
UPSTREAM_REVISION = "9620cc73f9c8e0ad003c514a5d3748f29611c4c0"
UNIT_IDS = ["OLP-0001"] + [f"OLP-{number:04d}" for number in range(4, 27)]
NS = {
    "container": "urn:oasis:names:tc:opendocument:xmlns:container",
    "opf": "http://www.idpf.org/2007/opf",
    "dc": "http://purl.org/dc/elements/1.1/",
    "xhtml": "http://www.w3.org/1999/xhtml",
    "math": "http://www.w3.org/1998/Math/MathML",
}
TOKEN_WORDS = {
    "element": "anggota", "formula": "formula", "derivation": "derivasi",
    "surjective": "surjektif", "injective": "injektif", "bijective": "bijektif",
    "surjection": "surjeksi", "injection": "injeksi", "bijection": "bijeksi",
}


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def normalize_member(base: PurePosixPath, href: str) -> tuple[str, str | None]:
    raw_path, separator, fragment = href.partition("#")
    if not raw_path:
        path = base.as_posix()
    else:
        path = (base.parent / raw_path).as_posix()
    parts: list[str] = []
    for part in PurePosixPath(path).parts:
        if part in ("", "."):
            continue
        if part == "..":
            if not parts:
                raise ValueError(f"Link escapes archive: {href}")
            parts.pop()
        else:
            parts.append(part)
    return "/".join(parts), fragment if separator else None


def prose_tokens(source: str) -> list[str]:
    source = re.sub(r"(?m)(?<!\\)%.*$", " ", source)
    source = re.sub(r"!!\^?a?\{([A-Za-z]+)\}(?:sne|s)?", lambda match: TOKEN_WORDS.get(match.group(1), " "), source)
    source = re.sub(r"\\begin\{(?:align\*?|multline\*?|tikzpicture|cases|array)\}.*?\\end\{(?:align\*?|multline\*?|tikzpicture|cases|array)\}", " ", source, flags=re.S)
    source = re.sub(r"\\\[.*?\\\]", " ", source, flags=re.S)
    source = re.sub(r"\$(?:\\.|[^$])*\$", " ", source, flags=re.S)
    source = re.sub(r"\\(?:documentclass|olfileid|olimport|ollabel|addcontentsline)(?:\[[^]]*\])?(?:\{[^{}]*\}){1,4}", " ", source)
    source = re.sub(r"\\olref(?:\[[^]]*\]){0,3}\{[^{}]*\}", " rujukan ", source)
    source = source.replace(r"\H{o}", "ő")
    source = re.sub(r"\\(?:begin|end)\{[^{}]*\}", " ", source)
    source = re.sub(r"\\[A-Za-z@]+\*?", " ", source)
    source = source.replace("{", " ").replace("}", " ").replace("~", " ")
    words = re.findall(r"[^\W\d_]{3,}", source.lower(), flags=re.UNICODE)
    stop = {"sfr", "set", "rel", "fun", "sec", "chap", "toc", "novice", "math", "assets", "diagrams", "tikz"}
    return [word for word in words if word not in stop]


def element_text_without_math(root: ET.Element) -> str:
    math_tag = "{" + NS["math"] + "}math"
    pieces: list[str] = []

    def walk(node: ET.Element) -> None:
        if node.tag == math_tag:
            return
        if node.text:
            pieces.append(node.text)
        for child in node:
            walk(child)
            if child.tail:
                pieces.append(child.tail)
    walk(root)
    return " ".join(pieces)


def audit(args: argparse.Namespace) -> dict:
    repo = Path(args.repo).resolve()
    epub = Path(args.epub).resolve()
    crosswalk_path = Path(args.crosswalk).resolve()
    package_manifest_path = Path(args.package_manifest).resolve()
    build_receipt_path = Path(args.build_receipt).resolve()
    findings: list[dict[str, str]] = []

    def require(condition: bool, code: str, detail: str) -> None:
        if not condition:
            findings.append({"code": code, "detail": detail})

    crosswalk = load_json(crosswalk_path)
    package_manifest = load_json(package_manifest_path)
    build_receipt = load_json(build_receipt_path)
    payload = epub.read_bytes()
    with zipfile.ZipFile(epub) as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        require(bool(infos) and infos[0].filename == "mimetype", "zip-mimetype-order", "mimetype must be first")
        require(bool(infos) and infos[0].compress_type == zipfile.ZIP_STORED, "zip-mimetype-compression", "mimetype must be stored")
        require(len(names) == len(set(names)), "zip-duplicate-path", "duplicate archive member")
        for name in names:
            path = PurePosixPath(name)
            require("\\" not in name and not path.is_absolute() and ".." not in path.parts and not re.match(r"^[A-Za-z]:", name), "zip-unsafe-path", name)
        require(archive.read("mimetype") == b"application/epub+zip", "zip-mimetype-value", "wrong mimetype")
        members = {name: archive.read(name) for name in names}

    require(build_receipt.get("status") == "PASS", "build-receipt-status", str(build_receipt.get("status")))
    require(build_receipt["outputs"]["epub"]["sha256"] == sha256(payload), "build-epub-hash", "build receipt hash mismatch")
    require(build_receipt["outputs"]["epub"]["bytes"] == len(payload), "build-epub-bytes", "build receipt size mismatch")
    require(build_receipt["outputs"]["content_crosswalk_sha256"] == sha256(crosswalk_path.read_bytes()), "crosswalk-hash", "crosswalk digest mismatch")
    require(build_receipt["outputs"]["package_manifest_sha256"] == sha256(package_manifest_path.read_bytes()), "package-manifest-hash", "package manifest digest mismatch")

    expected_entries = {row["path"]: row for row in package_manifest["entries"]}
    require(set(expected_entries) == set(members), "package-entry-set", "manifest/archive path set differs")
    for name, record in expected_entries.items():
        if name in members:
            require(record["bytes"] == len(members[name]), "package-entry-bytes", name)
            require(record["sha256"] == sha256(members[name]), "package-entry-hash", name)

    container = ET.fromstring(members["META-INF/container.xml"])
    rootfiles = container.findall(".//container:rootfile", NS)
    require(len(rootfiles) == 1, "container-rootfile-count", str(len(rootfiles)))
    opf_path = rootfiles[0].attrib.get("full-path", "") if rootfiles else ""
    require(opf_path == "EPUB/package.opf", "container-rootfile-path", opf_path)
    opf = ET.fromstring(members[opf_path])
    title = opf.findtext("opf:metadata/dc:title", namespaces=NS)
    language = opf.findtext("opf:metadata/dc:language", namespaces=NS)
    description = opf.findtext("opf:metadata/dc:description", namespaces=NS) or ""
    source = opf.findtext("opf:metadata/dc:source", namespaces=NS) or ""
    require(title == TITLE, "metadata-title", str(title))
    require(language == LANGUAGE, "metadata-language", str(language))
    require("24 saka 722" in description, "metadata-scope", description)
    require(UPSTREAM_REVISION in source, "metadata-upstream", source)
    require(any(meta.attrib.get("property") == "rendition:layout" and (meta.text or "") == "reflowable" for meta in opf.findall("opf:metadata/opf:meta", NS)), "metadata-reflowable", "missing rendition:layout")

    manifest_items = opf.findall("opf:manifest/opf:item", NS)
    by_id = {item.attrib["id"]: item for item in manifest_items}
    by_path: dict[str, ET.Element] = {}
    for item in manifest_items:
        target, _ = normalize_member(PurePosixPath(opf_path), item.attrib["href"])
        by_path[target] = item
        require(target in members, "manifest-missing-resource", target)
    require(len(by_id) == len(manifest_items), "manifest-duplicate-id", "duplicate item id")
    require(len(by_path) == len(manifest_items), "manifest-duplicate-href", "duplicate item href")
    exempt = {"mimetype", "META-INF/container.xml", opf_path}
    require(set(members) - exempt == set(by_path), "manifest-resource-set", "manifest does not cover all publication resources")

    spine_refs = [item.attrib.get("idref", "") for item in opf.findall("opf:spine/opf:itemref", NS)]
    require(len(spine_refs) == 26, "spine-count", str(len(spine_refs)))
    require(len(spine_refs) == len(set(spine_refs)), "spine-duplicates", "duplicate spine idref")
    require(all(ref in by_id for ref in spine_refs), "spine-missing-manifest-id", "unresolved idref")

    parsed: dict[str, ET.Element] = {}
    ids_by_path: dict[str, set[str]] = {}
    math_count = 0
    image_count = 0
    formula_ids: list[str] = []
    xhtml_paths = [path for path, item in by_path.items() if item.attrib.get("media-type") == "application/xhtml+xml"]
    for path in xhtml_paths:
        xhtml_payload = members[path]
        try:
            root = ET.fromstring(xhtml_payload)
        except ET.ParseError as error:
            findings.append({"code": "xhtml-parse", "detail": f"{path}: {error}"})
            continue
        require(
            not re.search(rb"<[A-Za-z_][\w.-]*:math\b", xhtml_payload),
            "prefixed-mathml-root",
            f"{path}: MathML roots must use the default namespace for HTML-reader interoperability",
        )
        parsed[path] = root
        ids = {element.attrib["id"] for element in root.iter() if "id" in element.attrib}
        ids_by_path[path] = ids
        require(root.tag == "{" + NS["xhtml"] + "}html", "xhtml-root", path)
        require(root.attrib.get("lang") == LANGUAGE, "xhtml-language", path)
        require(root.attrib.get("{http://www.w3.org/XML/1998/namespace}lang") == LANGUAGE, "xhtml-xml-language", path)
        require(not list(root.iter("{" + NS["xhtml"] + "}script")), "xhtml-script", path)
        body = root.find("xhtml:body", NS)
        require(body is not None and "".join(body.itertext()).strip() != "", "xhtml-empty-body", path)
        title_node = root.find("xhtml:head/xhtml:title", NS)
        require(title_node is not None and (title_node.text or "").strip() != "", "xhtml-empty-title", path)
        visible = element_text_without_math(root)
        require("!!" not in visible and not re.search(r"\\[A-Za-z@]+", visible), "xhtml-residual-source-markup", path)
        maths = list(root.iter("{" + NS["math"] + "}math"))
        math_count += len(maths)
        item = by_path[path]
        properties = set(item.attrib.get("properties", "").split())
        require(("mathml" in properties) == bool(maths), "manifest-mathml-property", path)
        for math in maths:
            alttext = math.attrib.get("alttext", "").strip()
            formula_id = math.attrib.get("data-formula-id", "").strip()
            require(bool(alttext), "math-alttext", path)
            require(bool(formula_id), "math-formula-id", path)
            if formula_id:
                formula_ids.append(formula_id)
            bad_identifiers = [node.text for node in math.iter("{" + NS["math"] + "}mi") if (node.text or "").startswith("\\")]
            require(not bad_identifiers, "math-unrendered-command", f"{path}:{bad_identifiers}")
        for image in root.iter("{" + NS["xhtml"] + "}img"):
            image_count += 1
            require(bool(image.attrib.get("alt", "").strip()), "image-alt", path)
            target, _ = normalize_member(PurePosixPath(path), image.attrib.get("src", ""))
            require(target in members, "image-target", f"{path} -> {target}")
        for element in root.iter():
            for attribute in ("href", "src"):
                href = element.attrib.get(attribute)
                if not href or href.startswith(("http://", "https://", "mailto:", "data:")):
                    continue
                target, fragment = normalize_member(PurePosixPath(path), href)
                require(target in members, "internal-link-target", f"{path} -> {href}")
                if fragment and target in ids_by_path:
                    require(fragment in ids_by_path[target], "internal-link-fragment", f"{path} -> {href}")

    # Resolve fragments after all documents have been indexed.
    for path, root in parsed.items():
        for element in root.iter():
            href = element.attrib.get("href")
            if not href or href.startswith(("http://", "https://", "mailto:", "data:")):
                continue
            target, fragment = normalize_member(PurePosixPath(path), href)
            if fragment and target in ids_by_path:
                require(fragment in ids_by_path[target], "internal-link-fragment", f"{path} -> {href}")

    require(len(formula_ids) == len(set(formula_ids)), "math-formula-id-unique", "duplicate formula ID")
    require(math_count == build_receipt["metrics"]["mathml_roots"], "math-count-build", f"{math_count}")
    require(image_count == build_receipt["metrics"]["figures"] + 1, "image-count-build", f"{image_count}")

    nav_path = next((path for path, item in by_path.items() if "nav" in item.attrib.get("properties", "").split()), "")
    require(nav_path == "EPUB/nav.xhtml", "nav-path", nav_path)
    nav = parsed.get(nav_path)
    toc_links = [] if nav is None else [node for node in nav.iter("{" + NS["xhtml"] + "}a") if "href" in node.attrib and not any(ancestor for ancestor in [])]
    require(len(toc_links) >= 26, "nav-link-count", str(len(toc_links)))

    manifest_rows = [json.loads(line) for line in (repo / "evidence" / "SOURCE_MANIFEST.jsonl").read_text(encoding="utf-8").splitlines() if line]
    source_manifest = {row["unit_id"]: row for row in manifest_rows}
    units = crosswalk.get("units", [])
    require([unit["unit_id"] for unit in units] == UNIT_IDS, "crosswalk-unit-order", "unit IDs or order drift")
    require(crosswalk.get("declared_scope", {}).get("reader_units") == 24 and crosswalk.get("declared_scope", {}).get("corpus_units") == 722, "crosswalk-scope", str(crosswalk.get("declared_scope")))
    crosswalk_math = 0
    crosswalk_images = 0
    coverage_values: list[float] = []
    for unit in units:
        unit_id = unit["unit_id"]
        source_path = repo / "translation" / unit["source_path"]
        source_bytes = source_path.read_bytes()
        require(sha256(source_bytes) == unit["translation_sha256"], "translation-source-hash", unit_id)
        require(unit["upstream_sha256"] == source_manifest[unit_id]["source_sha256"], "upstream-source-hash", unit_id)
        output = unit["output"]
        require(output in members, "crosswalk-output", output)
        root = parsed.get(output)
        if root is None:
            continue
        body = root.find("xhtml:body", NS)
        require(body is not None and body.attrib.get("data-source-unit") == unit_id, "source-unit-binding", unit_id)
        require(body is not None and body.attrib.get("data-source-sha256") == unit["translation_sha256"], "source-hash-binding", unit_id)
        document_math = list(root.iter("{" + NS["math"] + "}math"))
        alttexts = [node.attrib.get("alttext", "") for node in document_math]
        formula_records = unit.get("math", [])
        require([row["latex"] for row in formula_records] == alttexts, "formula-crosswalk-order", unit_id)
        for row in formula_records:
            require(row["latex_sha256"] == sha256(row["latex"].encode("utf-8")), "formula-crosswalk-hash", f"{unit_id}:{row.get('id')}")
        crosswalk_math += unit["mathml_roots"]
        crosswalk_images += unit["images"]
        source = source_bytes.decode("utf-8-sig")
        expected_structures = {name: len(re.findall(r"\\begin\{" + re.escape(name) + r"\}", source)) for name in ("defn", "ex", "prop", "thm", "prob", "proof")}
        for name, count in expected_structures.items():
            actual = len(root.findall(f".//xhtml:section[@class='semantic-block {name}']", NS))
            require(actual == count, "semantic-structure-count", f"{unit_id}:{name}:{actual}!={count}")
        expected_images = len(re.findall(r"\\olasset(?:\[[^]]*\])?\{", source)) + len(re.findall(r"\\begin\{tikzpicture\}", source))
        require(unit["images"] == expected_images, "diagram-source-coverage", f"{unit_id}:{unit['images']}!={expected_images}")
        if unit_id not in {"OLP-0004", "OLP-0011", "OLP-0020"}:
            expected_words = Counter(prose_tokens(source))
            rendered_words = Counter(re.findall(r"[^\W\d_]{3,}", element_text_without_math(root).lower(), flags=re.UNICODE))
            denominator = sum(expected_words.values())
            covered = sum(min(count, rendered_words[word]) for word, count in expected_words.items())
            ratio = covered / denominator if denominator else 1.0
            coverage_values.append(ratio)
            require(ratio >= 0.88, "prose-token-coverage", f"{unit_id}:{ratio:.4f}")
    require(crosswalk_math == math_count, "crosswalk-math-total", f"{crosswalk_math}!={math_count}")
    require(crosswalk_images == image_count - 1, "crosswalk-image-total", f"{crosswalk_images}!={image_count - 1}")

    epubcheck = load_json(Path(args.epubcheck_json).resolve())
    messages = epubcheck.get("messages", [])
    severities = Counter(message.get("severity", "UNKNOWN") for message in messages)
    require(not messages, "epubcheck-messages", json.dumps(dict(severities), sort_keys=True))

    cold = Path(args.cold_epub).resolve() if args.cold_epub else None
    if cold:
        require(cold.read_bytes() == payload, "cold-reproducibility", f"{sha256(payload)} != {sha256(cold.read_bytes())}")

    result = {
        "schema": "openlogic-jv-epub-independent-audit/1",
        "status": "PASS" if not findings else "FAIL",
        "artifact": {"path": epub.name, "bytes": len(payload), "sha256": sha256(payload)},
        "scope": {"reader_units": 24, "corpus_units": 722, "unit_ids": UNIT_IDS},
        "metrics": {
            "archive_entries": len(members), "spine_documents": len(spine_refs), "xhtml_documents": len(xhtml_paths),
            "mathml_roots_checked": math_count, "formula_ids_checked": len(formula_ids), "images_checked": image_count,
            "internal_documents_indexed": len(ids_by_path), "minimum_prose_token_coverage": min(coverage_values) if coverage_values else None,
            "epubcheck_messages": len(messages), "epubcheck_severities": dict(severities),
        },
        "cold_build": None if not cold else {"path": cold.name, "bytes": cold.stat().st_size, "sha256": sha256(cold.read_bytes()), "identical": cold.read_bytes() == payload},
        "findings": findings,
        "auditor": {"path": "tools/audit-epub.py", "sha256": sha256(Path(__file__).read_bytes()), "imports_producer_code": False},
    }
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    parser.add_argument("--epub", required=True)
    parser.add_argument("--crosswalk", required=True)
    parser.add_argument("--package-manifest", required=True)
    parser.add_argument("--build-receipt", required=True)
    parser.add_argument("--epubcheck-json", required=True)
    parser.add_argument("--cold-epub")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = audit(args)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
