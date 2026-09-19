#!/usr/bin/env python3
"""Build the bounded Javanese OpenLogic reader as deterministic EPUB 3.

The converter reads the accepted localized LaTeX directly.  It emits native
MathML, semantic XHTML, vector diagrams, a navigation document, and independent
build evidence.  It does not use the PDF as an input.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import uuid
import zipfile
from xml.etree import ElementTree as ET

from latex2mathml.converter import convert as latex_to_mathml
from pylatexenc.latexwalker import (
    LatexCharsNode,
    LatexCommentNode,
    LatexEnvironmentNode,
    LatexGroupNode,
    LatexMacroNode,
    LatexMathNode,
    LatexSpecialsNode,
    LatexWalker,
    get_default_latex_context_db,
)
from pylatexenc.macrospec import EnvironmentSpec, MacroSpec, MacroStandardArgsParser


SCHEMA = "openlogic-jv-epub-build/1"
VERSION = "0.2.0"
LANGUAGE = "jv-Latn-ID"
TITLE = "OpenLogic: Himpunan, Relasi, lan Fungsi"
SUBTITLE = "Wacan Basa Jawa, aksara Latin"
UPSTREAM_REVISION = "9620cc73f9c8e0ad003c514a5d3748f29611c4c0"
MODIFIED = "2026-09-13T00:00:00Z"
MATHML_NAMESPACE = "http://www.w3.org/1998/Math/MathML"
ET.register_namespace("", MATHML_NAMESPACE)
UNIT_IDS = ["OLP-0001"] + [f"OLP-{number:04d}" for number in range(4, 27)]
SOURCE_PATHS = {
    "OLP-0001": "content/open-logic-about.tex",
    "OLP-0004": "content/sets-functions-relations/sets/sets.tex",
    "OLP-0005": "content/sets-functions-relations/sets/basics.tex",
    "OLP-0006": "content/sets-functions-relations/sets/subsets.tex",
    "OLP-0007": "content/sets-functions-relations/sets/important-sets.tex",
    "OLP-0008": "content/sets-functions-relations/sets/unions-and-intersections.tex",
    "OLP-0009": "content/sets-functions-relations/sets/pairs-and-products.tex",
    "OLP-0010": "content/sets-functions-relations/sets/russells-paradox.tex",
    "OLP-0011": "content/sets-functions-relations/relations/relations-complete.tex",
    "OLP-0012": "content/sets-functions-relations/relations/relations-as-sets.tex",
    "OLP-0013": "content/sets-functions-relations/relations/reflections.tex",
    "OLP-0014": "content/sets-functions-relations/relations/special-properties.tex",
    "OLP-0015": "content/sets-functions-relations/relations/equivalence-relations.tex",
    "OLP-0016": "content/sets-functions-relations/relations/orders.tex",
    "OLP-0017": "content/sets-functions-relations/relations/graphs.tex",
    "OLP-0018": "content/sets-functions-relations/relations/trees.tex",
    "OLP-0019": "content/sets-functions-relations/relations/operations.tex",
    "OLP-0020": "content/sets-functions-relations/functions/functions.tex",
    "OLP-0021": "content/sets-functions-relations/functions/function-basics.tex",
    "OLP-0022": "content/sets-functions-relations/functions/function-kinds.tex",
    "OLP-0023": "content/sets-functions-relations/functions/functions-relations.tex",
    "OLP-0024": "content/sets-functions-relations/functions/inverses.tex",
    "OLP-0025": "content/sets-functions-relations/functions/composition.tex",
    "OLP-0026": "content/sets-functions-relations/functions/partial-functions.tex",
}
CHAPTER_CHILDREN = {
    "OLP-0004": [f"OLP-{number:04d}" for number in range(5, 11)],
    "OLP-0011": [f"OLP-{number:04d}" for number in range(12, 20)],
    "OLP-0020": [f"OLP-{number:04d}" for number in range(21, 27)],
}
TYPE_LABELS = {
    "defn": "Definisi",
    "ex": "Tuladha",
    "prop": "Proposisi",
    "thm": "Teorema",
    "prob": "Soal",
    "proof": "Bukti",
    "intro": "Pambuka",
    "digress": "Cathetan",
}
TOKEN_BASE = {
    "element": "anggota",
    "formula": "formula",
    "derivation": "derivasi",
    "surjective": "surjektif",
    "injective": "injektif",
    "bijective": "bijektif",
    "surjection": "surjeksi",
    "injection": "injeksi",
    "bijection": "bijeksi",
}
TOKEN_ARTICLE = {
    "element": "salah siji anggota",
    "formula": "salah siji formula",
    "derivation": "salah siji derivasi",
    "surjection": "salah siji surjeksi",
    "injection": "salah siji injeksi",
    "bijection": "salah siji bijeksi",
    "surjective": "surjektif",
    "injective": "injektif",
    "bijective": "bijektif",
}
DIAGRAM_ALT = {
    "union": "Rong himpunan A lan B kang tumpang tindih; kabeh dhaerah A lan B disorot kanggo nuduhake gabungan A ∪ B.",
    "intersection": "Rong himpunan A lan B kang tumpang tindih; mung dhaerah tumpang tindih disorot kanggo nuduhake irisan A ∩ B.",
    "difference": "Rong himpunan A lan B kang tumpang tindih; bagean A ing njaba B disorot kanggo nuduhake selisih A minus B.",
    "function": "Pemetaan saka telung anggota domain A menyang anggota kodomain B; saben anggota A duwe persis siji panah metu.",
    "surjective": "Fungsi saka A menyang B kang saben anggota kodomain B dituju paling ora siji panah.",
    "injective": "Fungsi saka A menyang B kang saben panah saka argumen beda tumuju nilai beda; siji anggota kodomain ora dituju.",
    "bijective": "Fungsi saka A menyang B kang masangake saben anggota loro himpunan kanthi siji-menyang-siji.",
    "composition": "Telung himpunan A, B, lan C kanthi panah f saka A menyang B, g saka B menyang C, lan g komposisi f saka A menyang C.",
    "graph-one": "Graf mawa arah kanthi simpul 1, 2, 3, lan 4; rusuke 1 menyang 1, 1 menyang 2, 1 menyang 3, lan 2 menyang 3; simpul 4 kapisah.",
    "graph-two": "Graf mawa arah kanthi simpul 1, 2, lan 3; rusuke 1 menyang 1, 1 menyang 2, 1 menyang 3, lan 2 menyang 3.",
    "tree": "Wit kanthi oyod r; anak r yaiku a lan b; anak a yaiku c, d, lan e.",
}


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json(data: object) -> bytes:
    return (json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def resolve_tokens(text: str) -> str:
    def article_cap(match: re.Match[str]) -> str:
        value = TOKEN_ARTICLE[match.group(1)]
        return value[:1].upper() + value[1:]

    def base_cap(match: re.Match[str]) -> str:
        value = TOKEN_BASE[match.group(1)]
        return value[:1].upper() + value[1:]

    text = re.sub(r"!!\^a\{([A-Za-z]+)\}", article_cap, text)
    text = re.sub(r"!!\^\{([A-Za-z]+)\}", base_cap, text)
    text = re.sub(r"!!a\{([A-Za-z]+)\}", lambda match: TOKEN_ARTICLE[match.group(1)], text)
    text = re.sub(r"!!\{([A-Za-z]+)\}sne", lambda match: TOKEN_BASE[match.group(1)] + "ne", text)
    text = re.sub(r"!!\{([A-Za-z]+)\}s", lambda match: TOKEN_BASE[match.group(1)], text)
    text = re.sub(r"!!\{([A-Za-z]+)\}", lambda match: TOKEN_BASE[match.group(1)], text)
    if "!!" in text:
        raise ValueError("Unresolved OpenLogic token marker")
    return text


def context_db():
    context = get_default_latex_context_db()
    macros = [
        MacroSpec("href", MacroStandardArgsParser(argspec="{{")),
        MacroSpec("footnote", MacroStandardArgsParser(argspec="{")),
        MacroSpec("citeyear", MacroStandardArgsParser(argspec="{")),
        MacroSpec("caption", MacroStandardArgsParser(argspec="{")),
        MacroSpec("olfileid", MacroStandardArgsParser(argspec="[{{{")),
        MacroSpec("olchapter", MacroStandardArgsParser(argspec="[{{{")),
        MacroSpec("olsection", MacroStandardArgsParser(argspec="[{")),
        MacroSpec("olimport", MacroStandardArgsParser(argspec="[{")),
        MacroSpec("ollabel", MacroStandardArgsParser(argspec="{")),
        MacroSpec("olref", MacroStandardArgsParser(argspec="[[[{")),
        MacroSpec("Olref", MacroStandardArgsParser(argspec="[[[{")),
        MacroSpec("oliflabeldef", MacroStandardArgsParser(argspec="{{{")),
        MacroSpec("olasset", MacroStandardArgsParser(argspec="[{")),
        MacroSpec("jvchapterstar", MacroStandardArgsParser(argspec="{")),
        MacroSpec("H", MacroStandardArgsParser(argspec="{")),
        MacroSpec("Setabs", MacroStandardArgsParser(argspec="{{")),
        MacroSpec("tuple", MacroStandardArgsParser(argspec="{")),
        MacroSpec("Pow", MacroStandardArgsParser(argspec="{")),
        MacroSpec("dom", MacroStandardArgsParser(argspec="{")),
        MacroSpec("ran", MacroStandardArgsParser(argspec="{")),
        MacroSpec("len", MacroStandardArgsParser(argspec="{")),
        MacroSpec("comp", MacroStandardArgsParser(argspec="{{")),
        MacroSpec("Id", MacroStandardArgsParser(argspec="{")),
        MacroSpec("funimage", MacroStandardArgsParser(argspec="{{")),
        MacroSpec("funrestrictionto", MacroStandardArgsParser(argspec="{{")),
        MacroSpec("equivrep", MacroStandardArgsParser(argspec="{{")),
        MacroSpec("equivclass", MacroStandardArgsParser(argspec="{{")),
    ]
    environments = [
        EnvironmentSpec(name, MacroStandardArgsParser(argspec="["))
        for name in ("defn", "ex", "prop", "thm", "prob")
    ] + [
        EnvironmentSpec(name)
        for name in ("proof", "explain", "intro", "digress", "figure", "document", "center")
    ] + [
        EnvironmentSpec("tagblock", MacroStandardArgsParser(argspec="{")),
        EnvironmentSpec("tikzpicture", MacroStandardArgsParser(argspec="[")),
    ]
    context.add_context_category("jv-openlogic", macros=macros, environments=environments, prepend=True)
    return context


def arg_node(node: LatexMacroNode | LatexEnvironmentNode, index: int):
    args = getattr(getattr(node, "nodeargd", None), "argnlist", [])
    return args[index] if index < len(args) else None


def arg_latex(node: LatexMacroNode | LatexEnvironmentNode, index: int) -> str:
    arg = arg_node(node, index)
    if arg is None:
        return ""
    if isinstance(arg, LatexGroupNode):
        return "".join(child.latex_verbatim() for child in arg.nodelist)
    return arg.latex_verbatim()


def sanitize_id(value: str) -> str:
    base = re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-.").lower()
    return base or "anchor"


def strip_tags(fragment: str) -> str:
    text = re.sub(r"<math\b[^>]*\balttext=\"([^\"]*)\"[^>]*>.*?</math>", r" \1 ", fragment, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def balanced_group(source: str, start: int) -> tuple[str, int] | None:
    cursor = start
    while cursor < len(source) and source[cursor].isspace():
        cursor += 1
    if cursor >= len(source) or source[cursor] != "{":
        return None
    depth = 1
    index = cursor + 1
    while index < len(source):
        if source[index] == "\\":
            index += 2
            continue
        if source[index] == "{":
            depth += 1
        elif source[index] == "}":
            depth -= 1
            if depth == 0:
                return source[cursor + 1:index], index + 1
        index += 1
    raise ValueError("Unbalanced mathematical macro argument")


def replace_math_macro(source: str, name: str, arity: int, replacement) -> str:
    needle = "\\" + name
    cursor = 0
    pieces: list[str] = []
    while True:
        match = re.search(re.escape(needle) + r"(?![A-Za-z@])", source[cursor:])
        if not match:
            pieces.append(source[cursor:])
            break
        start = cursor + match.start()
        end_name = cursor + match.end()
        pieces.append(source[cursor:start])
        args: list[str] = []
        end = end_name
        valid = True
        for _ in range(arity):
            parsed = balanced_group(source, end)
            if parsed is None:
                valid = False
                break
            value, end = parsed
            args.append(normalize_math(value))
        if not valid:
            pieces.append(source[start:end_name])
            cursor = end_name
            continue
        pieces.append(replacement(*args))
        cursor = end
    return "".join(pieces)


def normalize_math(source: str) -> str:
    source = resolve_tokens(source)
    transforms = [
        ("tuple", 1, lambda value: r"\left\langle " + value + r" \right\rangle"),
        ("Setabs", 2, lambda left, right: r"\left\{ " + left + r" : " + right + r" \right\}"),
        ("Pow", 1, lambda value: r"\wp(" + value + ")"),
        ("dom", 1, lambda value: r"\mathrm{dom}(" + value + ")"),
        ("ran", 1, lambda value: r"\mathrm{ran}(" + value + ")"),
        ("len", 1, lambda value: r"\mathrm{len}(" + value + ")"),
        ("comp", 2, lambda first, second: second + r" \circ " + first),
        ("Id", 1, lambda value: r"\mathrm{Id}_{" + value + "}"),
        ("funimage", 2, lambda function, domain: function + "[" + domain + "]"),
        ("funrestrictionto", 2, lambda function, domain: function + r"\upharpoonright_{" + domain + "}"),
        ("equivrep", 2, lambda value, relation: "[" + value + r"]_{" + relation + "}"),
        ("equivclass", 2, lambda value, relation: value + r"/_{" + relation + "}"),
        ("nicefrac", 2, lambda numerator, denominator: r"\frac{" + numerator + "}{" + denominator + "}"),
        ("shoveleft", 1, lambda value: value),
        ("shoveright", 1, lambda value: value),
    ]
    for name, arity, replacement in transforms:
        source = replace_math_macro(source, name, arity, replacement)
    atom_replacements = {
        r"\Nat": r"\mathbb{N}",
        r"\Int": r"\mathbb{Z}",
        r"\PosInt": r"\mathbb{Z}^{+}",
        r"\Real": r"\mathbb{R}",
        r"\Rat": r"\mathbb{Q}",
        r"\Bin": r"\mathbb{B}",
        r"\emptyseq": r"\Lambda",
        r"\fdefined": r"\downarrow",
        r"\fundefined": r"\uparrow",
        r"\pto": r"\rightharpoonup",
        r"\restriction": r"\upharpoonright",
        r"\liff": r"\leftrightarrow",
        r"\lif": r"\rightarrow",
    }
    for old, new in atom_replacements.items():
        source = re.sub(re.escape(old) + r"(?![A-Za-z@])", lambda _: new, source)
    source = source.replace(r"\allowbreak", "")
    source = source.replace(r"\textrm", r"\mathrm")
    source = source.replace("\t", " ")
    source = source.replace("~", r"\,")
    return re.sub(r"[ \t]+", " ", source).strip()


def mathml(source: str, display: bool, formula_id: str) -> str:
    normalized = normalize_math(source)
    rendered = latex_to_mathml(normalized, display="block" if display else "inline")
    root = ET.fromstring(rendered)
    root.set("alttext", normalized)
    root.set("data-formula-id", formula_id)
    return ET.tostring(root, encoding="unicode", short_empty_elements=True)


def split_align_rows(source: str) -> list[list[str]]:
    rows: list[str] = []
    current: list[str] = []
    depth = 0
    index = 0
    while index < len(source):
        char = source[index]
        if char == "{" and (index == 0 or source[index - 1] != "\\"):
            depth += 1
        elif char == "}" and (index == 0 or source[index - 1] != "\\"):
            depth = max(0, depth - 1)
        if depth == 0 and source[index:index + 2] == r"\\":
            rows.append("".join(current))
            current = []
            index += 2
            continue
        current.append(char)
        index += 1
    rows.append("".join(current))
    result: list[list[str]] = []
    for row in rows:
        cells: list[str] = []
        cell: list[str] = []
        depth = 0
        for index, char in enumerate(row):
            if char == "{" and (index == 0 or row[index - 1] != "\\"):
                depth += 1
            elif char == "}" and (index == 0 or row[index - 1] != "\\"):
                depth = max(0, depth - 1)
            if char == "&" and depth == 0:
                cells.append("".join(cell))
                cell = []
            else:
                cell.append(char)
        cells.append("".join(cell))
        if any(value.strip() for value in cells):
            result.append(cells)
    return result


def align_mathml(source: str, environment: str, formula_id: str) -> str:
    inner = re.sub(r"^\s*\\begin\{" + re.escape(environment) + r"\}", "", source)
    inner = re.sub(r"\\end\{" + re.escape(environment) + r"\}\s*$", "", inner)
    normalized = normalize_math(inner)
    root = ET.Element(f"{{{MATHML_NAMESPACE}}}math", {
        "display": "block",
        "alttext": normalized,
        "data-formula-id": formula_id,
    })
    table = ET.SubElement(root, f"{{{MATHML_NAMESPACE}}}mtable")
    for row in split_align_rows(normalized):
        tr = ET.SubElement(table, f"{{{MATHML_NAMESPACE}}}mtr")
        for value in row:
            td = ET.SubElement(tr, f"{{{MATHML_NAMESPACE}}}mtd")
            fragment = ET.fromstring(latex_to_mathml(value.strip() or r"\phantom{0}"))
            for child in list(fragment):
                td.append(child)
    return ET.tostring(root, encoding="unicode", short_empty_elements=True)


def current_git_commit(repo: Path) -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()


class Renderer:
    def __init__(self, unit_id: str, prefix: tuple[str, str, str], labels: dict[str, dict[str, str]]):
        self.unit_id = unit_id
        self.prefix = prefix
        self.labels = labels
        self.unknown_macros: set[str] = set()
        self.unknown_environments: set[str] = set()
        self.math_sources: list[dict[str, str | bool]] = []
        self.environment_counts: dict[str, int] = {}
        self.image_count = 0
        self.footnote_counter = 0
        self.tikz_counter = 0
        self.title = unit_id

    def next_formula_id(self, source: str, display: bool) -> str:
        formula_id = f"formula-{self.unit_id.lower()}-{len(self.math_sources) + 1:04d}"
        normalized = normalize_math(source)
        self.math_sources.append({
            "id": formula_id,
            "display": display,
            "latex": normalized,
            "latex_sha256": sha256_bytes(normalized.encode("utf-8")),
        })
        return formula_id

    def label_target(self, node: LatexMacroNode) -> str:
        options = [arg_latex(node, index).strip() for index in range(3)]
        label = arg_latex(node, 3).strip()
        part, chapter, section = self.prefix
        if not options[0]:
            return f"{part}:{chapter}:{section}:{label}"
        if not options[1]:
            return f"{part}:{chapter}:{options[0]}:{label}"
        if not options[2]:
            return f"{part}:{options[0]}:{options[1]}:{label}"
        return f"{options[0]}:{options[1]}:{options[2]}:{label}"

    def local_label(self, value: str) -> str:
        part, chapter, section = self.prefix
        return f"{part}:{chapter}:{section}:{value}"

    def render_inline(self, nodes) -> str:
        pieces: list[str] = []
        for node in nodes or []:
            if isinstance(node, LatexCharsNode):
                value = resolve_tokens(node.chars)
                value = value.replace("---", "—").replace("--", "–")
                value = re.sub(r"\s+", " ", value)
                pieces.append(html.escape(value))
            elif isinstance(node, LatexCommentNode):
                continue
            elif isinstance(node, LatexGroupNode):
                pieces.append(self.render_inline(node.nodelist))
            elif isinstance(node, LatexSpecialsNode):
                pieces.append("&#160;" if node.specials_chars == "~" else html.escape(node.specials_chars))
            elif isinstance(node, LatexMathNode):
                source = node.latex_verbatim()
                if source.startswith("$") and source.endswith("$"):
                    source = source[1:-1]
                elif source.startswith(r"\(") and source.endswith(r"\)"):
                    source = source[2:-2]
                elif source.startswith(r"\[") and source.endswith(r"\]"):
                    source = source[2:-2]
                display = getattr(node, "displaytype", "inline") == "display"
                formula_id = self.next_formula_id(source, display)
                pieces.append(mathml(source, display, formula_id))
            elif isinstance(node, LatexMacroNode):
                pieces.append(self.render_macro(node, inline=True))
            elif isinstance(node, LatexEnvironmentNode):
                pieces.append(self.render_environment(node, inline=True))
        return "".join(pieces)

    def render_macro(self, node: LatexMacroNode, inline: bool) -> str:
        name = node.macroname
        if name in {"emph", "textit"}:
            return f"<em>{self.render_arg(node, 0)}</em>"
        if name in {"textbf", "mathbf"}:
            return f"<strong>{self.render_arg(node, 0)}</strong>"
        if name in {"text", "textrm", "mbox", "shoveleft", "shoveright"}:
            return self.render_arg(node, 0)
        if name == "href":
            url = strip_tags(self.render_arg(node, 0))
            if not re.match(r"^https?://", url):
                raise ValueError(f"Unsafe href in {self.unit_id}: {url}")
            return f'<a href="{html.escape(url, quote=True)}">{self.render_arg(node, 1)}</a>'
        if name == "footnote":
            self.footnote_counter += 1
            footnote_id = f"fn-{self.unit_id.lower()}-{self.footnote_counter}"
            return (
                f'<a class="noteref" epub:type="noteref" href="#{footnote_id}">[{self.footnote_counter}]</a>'
                f'<span class="footnote" epub:type="footnote" id="{footnote_id}">{self.render_arg(node, 0)}</span>'
            )
        if name == "citeyear":
            key = strip_tags(self.render_arg(node, 0))
            if key != "Benacerraf1965":
                raise ValueError(f"Unhandled citation key: {key}")
            return '<a class="citation" href="bibliography.xhtml#bib-benacerraf1965">1965</a>'
        if name == "ollabel":
            target = self.local_label(strip_tags(self.render_arg(node, 0)))
            return f'<span id="{sanitize_id(target)}" class="anchor"></span>'
        if name in {"olref", "Olref"}:
            target = self.label_target(node)
            if target not in self.labels:
                raise ValueError(f"Reference target outside EPUB scope: {target} in {self.unit_id}")
            record = self.labels[target]
            return f'<a class="xref" href="{record["href"]}">{html.escape(record["text"])}</a>'
        if name == "oliflabeldef":
            target = strip_tags(self.render_arg(node, 0))
            return self.render_arg(node, 1 if target in self.labels else 2)
        if name == "H":
            value = strip_tags(self.render_arg(node, 0))
            return {"o": "ő", "O": "Ő", "u": "ű", "U": "Ű"}.get(value, html.escape(value))
        if name in {"ldots", "dots", "vdots", "ddots"}:
            return "…"
        if name in {"allowbreak", "OLEndChapterHook", "documentclass", "olfileid", "olimport", "addcontentsline", "phantom"}:
            return "" if name != "phantom" else self.render_arg(node, 0)
        if name in {"jvchapterstar", "olchapter", "olsection", "chapter"}:
            return ""
        if name == "caption":
            return self.render_arg(node, 0)
        if name in {"%", "#", "_", "&", "$", "{" , "}"}:
            return html.escape(name)
        if name == "\\":
            return "<br/>"
        args = getattr(getattr(node, "nodeargd", None), "argnlist", [])
        if args and any(arg is not None for arg in args):
            self.unknown_macros.add(name)
            return "".join(self.render_inline(arg.nodelist if isinstance(arg, LatexGroupNode) else [arg]) for arg in args if arg)
        self.unknown_macros.add(name)
        return ""

    def render_arg(self, node: LatexMacroNode | LatexEnvironmentNode, index: int) -> str:
        arg = arg_node(node, index)
        if arg is None:
            return ""
        return self.render_inline(arg.nodelist if isinstance(arg, LatexGroupNode) else [arg])

    def render_flow(self, nodes) -> str:
        blocks: list[str] = []
        pending: list[str] = []

        def flush() -> None:
            value = re.sub(r"\s+", " ", "".join(pending)).strip()
            pending.clear()
            if value:
                blocks.append(f"<p>{value}</p>")

        for node in nodes or []:
            if isinstance(node, LatexCharsNode):
                chunks = re.split(r"\n\s*\n", node.chars)
                for index, chunk in enumerate(chunks):
                    if chunk:
                        value = resolve_tokens(chunk).replace("---", "—").replace("--", "–")
                        pending.append(html.escape(re.sub(r"\s+", " ", value)))
                    if index + 1 < len(chunks):
                        flush()
            elif isinstance(node, LatexCommentNode):
                continue
            elif isinstance(node, LatexMathNode):
                source = node.latex_verbatim()
                if source.startswith("$") and source.endswith("$"):
                    source = source[1:-1]
                elif source.startswith(r"\[") and source.endswith(r"\]"):
                    source = source[2:-2]
                display = getattr(node, "displaytype", "inline") == "display"
                formula_id = self.next_formula_id(source, display)
                rendered = mathml(source, display, formula_id)
                if display:
                    flush()
                    blocks.append(f'<div class="math-display">{rendered}</div>')
                else:
                    pending.append(rendered)
            elif isinstance(node, LatexMacroNode) and node.macroname in {"jvchapterstar", "olchapter", "olsection", "chapter"}:
                flush()
                if node.macroname == "olchapter":
                    title = strip_tags(self.render_arg(node, 3))
                    anchor = sanitize_id(f"{strip_tags(self.render_arg(node, 1))}:{strip_tags(self.render_arg(node, 2))}::chap")
                    level = 1
                elif node.macroname == "olsection":
                    title = strip_tags(self.render_arg(node, 1))
                    anchor = sanitize_id(":".join(self.prefix) + ":sec")
                    level = 2
                else:
                    title = strip_tags(self.render_arg(node, 0))
                    anchor = sanitize_id(self.unit_id + ":frontmatter")
                    level = 1
                self.title = title
                blocks.append(f'<h{level} id="{anchor}">{html.escape(title)}</h{level}>')
            elif isinstance(node, LatexEnvironmentNode):
                flush()
                blocks.append(self.render_environment(node, inline=False))
            elif isinstance(node, LatexGroupNode):
                pending.append(self.render_inline(node.nodelist))
            elif isinstance(node, LatexSpecialsNode):
                pending.append("&#160;" if node.specials_chars == "~" else html.escape(node.specials_chars))
            elif isinstance(node, LatexMacroNode):
                pending.append(self.render_macro(node, inline=True))
        flush()
        return "\n".join(block for block in blocks if block)

    def render_environment(self, node: LatexEnvironmentNode, inline: bool) -> str:
        name = node.environmentname
        self.environment_counts[name] = self.environment_counts.get(name, 0) + 1
        if name == "document" or name == "tagblock":
            return self.render_flow(node.nodelist)
        if name in TYPE_LABELS:
            title = TYPE_LABELS[name]
            optional = strip_tags(self.render_arg(node, 0))
            heading = title + (f": {optional}" if optional else "")
            body = self.render_flow(node.nodelist)
            role = "doc-example" if name == "ex" else ("doc-qna" if name == "prob" else "doc-notice")
            return f'<section class="semantic-block {name}" role="{role}"><h3>{html.escape(heading)}</h3>{body}</section>'
        if name == "explain":
            return f'<aside class="explain">{self.render_flow(node.nodelist)}</aside>'
        if name in {"intro", "digress"}:
            return f'<aside class="{name}"><h3>{TYPE_LABELS[name]}</h3>{self.render_flow(node.nodelist)}</aside>'
        if name == "enumerate":
            items: list[list] = []
            current: list = []
            for child in node.nodelist:
                if isinstance(child, LatexMacroNode) and child.macroname == "item":
                    if current:
                        items.append(current)
                    current = []
                else:
                    current.append(child)
            if current:
                items.append(current)
            return "<ol>" + "".join(f"<li>{self.render_flow(item)}</li>" for item in items) + "</ol>"
        if name == "figure":
            return self.render_figure(node)
        if name == "center":
            if any(isinstance(child, LatexEnvironmentNode) and child.environmentname == "tikzpicture" for child in node.nodelist):
                return self.diagram("tree", None)
            return f'<div class="center">{self.render_flow(node.nodelist)}</div>'
        if name in {"align", "align*", "multline", "multline*"}:
            raw = node.latex_verbatim()
            if "tikzpicture" in raw and self.unit_id == "OLP-0017":
                marker = raw.find(r"\intertext")
                parsed = balanced_group(raw, marker + len(r"\intertext")) if marker >= 0 else None
                intertext = "Iki beda karo graf kanthi simpul 1, 2, lan 3." if parsed is None else self.render_fragment(parsed[0])
                return self.diagram("graph-one", None) + f"<p>{intertext}</p>" + self.diagram("graph-two", None)
            inner = re.sub(r"^\s*\\begin\{" + re.escape(name) + r"\}", "", raw)
            inner = re.sub(r"\\end\{" + re.escape(name) + r"\}\s*$", "", inner)
            formula_id = self.next_formula_id(inner, True)
            return f'<div class="math-display">{align_mathml(raw, name, formula_id)}</div>'
        if name == "tikzpicture":
            self.tikz_counter += 1
            key = "tree" if self.unit_id == "OLP-0018" else ("graph-one" if self.tikz_counter == 1 else "graph-two")
            return self.diagram(key, None)
        self.unknown_environments.add(name)
        return self.render_flow(node.nodelist)

    def render_fragment(self, source: str) -> str:
        nodes, _, _ = LatexWalker(source, latex_context=context_db()).get_latex_nodes()
        return self.render_inline(nodes)

    def diagram(self, key: str, caption: str | None, label: str | None = None) -> str:
        self.image_count += 1
        anchor = f' id="{sanitize_id(label)}"' if label else ""
        caption_html = f"<figcaption>{caption}</figcaption>" if caption else ""
        return (
            f'<figure{anchor}><img src="../images/{key}.svg" alt="{html.escape(DIAGRAM_ALT[key], quote=True)}"/>'
            f"{caption_html}</figure>"
        )

    def render_figure(self, node: LatexEnvironmentNode) -> str:
        asset = ""
        caption = ""
        label = ""
        for child in node.nodelist:
            if isinstance(child, LatexMacroNode) and child.macroname == "olasset":
                asset = strip_tags(self.render_arg(child, 1))
            elif isinstance(child, LatexMacroNode) and child.macroname == "caption":
                caption = self.render_arg(child, 0)
            elif isinstance(child, LatexMacroNode) and child.macroname == "ollabel":
                label = self.local_label(strip_tags(self.render_arg(child, 0)))
        key = Path(asset).stem
        if key not in DIAGRAM_ALT:
            raise ValueError(f"Unknown figure asset in {self.unit_id}: {asset}")
        return self.diagram(key, caption, label or None)


def discover_prefix(source: str, unit_id: str) -> tuple[str, str, str]:
    match = re.search(r"\\olfileid(?:\[[^]]*\])?\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}", source)
    if match:
        return tuple(match.groups())  # type: ignore[return-value]
    chapter = {"OLP-0004": "set", "OLP-0011": "rel", "OLP-0020": "fun"}.get(unit_id)
    if chapter:
        return "sfr", chapter, ""
    return "front", "about", unit_id.lower()


def discover_title(source: str, unit_id: str) -> str:
    patterns = [
        r"\\olsection(?:\[[^]]*\])?\{([^{}]*)\}",
        r"\\olchapter(?:\[[^]]*\])?\{[^{}]*\}\{[^{}]*\}\{([^{}]*)\}",
        r"\\chapter\*?\{([^{}]*)\}",
    ]
    for pattern in patterns:
        match = re.search(pattern, source)
        if match:
            return resolve_tokens(match.group(1)).replace(r"\H{o}", "ő")
    return unit_id


def discover_labels(sources: dict[str, str], titles: dict[str, str]) -> dict[str, dict[str, str]]:
    labels: dict[str, dict[str, str]] = {}
    for unit_id, source in sources.items():
        prefix = discover_prefix(source, unit_id)
        href = f"{unit_id.lower()}.xhtml"
        if unit_id in CHAPTER_CHILDREN:
            target = f"{prefix[0]}:{prefix[1]}::chap"
            labels[target] = {"href": href + "#" + sanitize_id(target), "text": f'bab “{titles[unit_id]}”'}
        elif unit_id != "OLP-0001":
            target = ":".join(prefix) + ":sec"
            labels[target] = {"href": href + "#" + sanitize_id(target), "text": f'perangan “{titles[unit_id]}”'}
        for match in re.finditer(r"\\ollabel\{([^}]+)\}", source):
            full = ":".join(prefix) + ":" + match.group(1)
            local = match.group(1)
            if local.startswith("fig") or local == "difference":
                kind = "gambar"
            elif local.startswith("prop") or local == "cardnmprod":
                kind = "proposisi"
            elif local.startswith("thm"):
                kind = "teorema"
            elif local.startswith("example"):
                kind = "tuladha"
            else:
                kind = "definisi"
            labels[full] = {"href": href + "#" + sanitize_id(full), "text": f'{kind} ing perangan “{titles[unit_id]}”'}
    return labels


def xhtml_document(title: str, body: str, source_unit: str | None = None, source_sha: str | None = None) -> str:
    attrs = ""
    if source_unit and source_sha:
        attrs = f' data-source-unit="{source_unit}" data-source-sha256="{source_sha}"'
    return f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="{LANGUAGE}" xml:lang="{LANGUAGE}">
<head><meta charset="utf-8"/><title>{html.escape(title)}</title><link rel="stylesheet" type="text/css" href="../css/book.css"/></head>
<body{attrs}><main>{body}</main></body>
</html>
'''


def diagram_svg(key: str) -> str:
    title = html.escape(DIAGRAM_ALT[key])
    head = f'<svg xmlns="http://www.w3.org/2000/svg" role="img" viewBox="0 0 640 300"><title>{title}</title><desc>{title}</desc><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#263238"/></marker><pattern id="hatch" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M0,10 L10,0" stroke="#7e57c2" stroke-width="3"/></pattern></defs><rect width="640" height="300" fill="#fff"/>'
    tail = "</svg>\n"
    if key in {"union", "intersection", "difference"}:
        fill_a = "url(#hatch)" if key in {"union", "difference"} else "#fff"
        fill_b = "url(#hatch)" if key == "union" else "#fff"
        body = f'<ellipse cx="255" cy="150" rx="145" ry="105" fill="{fill_a}" stroke="#37474f" stroke-width="4"/><ellipse cx="385" cy="150" rx="145" ry="105" fill="{fill_b}" stroke="#37474f" stroke-width="4"/>'
        if key == "intersection":
            body += '<path d="M320 62 A145 105 0 0 0 320 238 A145 105 0 0 0 320 62" fill="url(#hatch)" stroke="none"/>'
        if key == "difference":
            body += '<ellipse cx="385" cy="150" rx="145" ry="105" fill="#fff" stroke="#37474f" stroke-width="4"/>'
        body += '<text x="190" y="155" font-size="34">A</text><text x="435" y="155" font-size="34">B</text>'
        return head + body + tail
    if key in {"function", "surjective", "injective", "bijective"}:
        left = [(150, 75), (150, 150), (150, 225)]
        right = [(490, 75), (490, 150), (490, 225)]
        mappings = {
            "function": [(0, 0), (1, 1), (2, 1)],
            "surjective": [(0, 0), (1, 1), (2, 1)],
            "injective": [(0, 0), (1, 1)],
            "bijective": [(0, 0), (1, 1), (2, 2)],
        }[key]
        body = '<ellipse cx="150" cy="150" rx="90" ry="135" fill="none" stroke="#37474f" stroke-width="4"/><ellipse cx="490" cy="150" rx="90" ry="135" fill="none" stroke="#37474f" stroke-width="4"/><text x="140" y="32" font-size="28">A</text><text x="480" y="32" font-size="28">B</text>'
        body += "".join(f'<circle cx="{x}" cy="{y}" r="10" fill="#5e35b1"/>' for x, y in left + right)
        body += "".join(f'<line x1="{left[a][0]+12}" y1="{left[a][1]}" x2="{right[b][0]-14}" y2="{right[b][1]}" stroke="#263238" stroke-width="4" marker-end="url(#arrow)"/>' for a, b in mappings)
        return head + body + tail
    if key == "composition":
        centers = [100, 320, 540]
        body = "".join(f'<ellipse cx="{x}" cy="150" rx="70" ry="120" fill="none" stroke="#37474f" stroke-width="4"/><text x="{x-10}" y="45" font-size="28">{label}</text>' for x, label in zip(centers, "ABC"))
        for y in (105, 195):
            body += "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="#5e35b1"/>' for x in centers)
            body += f'<line x1="112" y1="{y}" x2="306" y2="{y}" stroke="#263238" stroke-width="4" marker-end="url(#arrow)"/><line x1="332" y1="{y}" x2="526" y2="{y}" stroke="#263238" stroke-width="4" marker-end="url(#arrow)"/>'
        body += '<text x="205" y="90" font-size="24">f</text><text x="425" y="90" font-size="24">g</text><path d="M110 250 Q320 305 530 250" fill="none" stroke="#7e57c2" stroke-width="4" marker-end="url(#arrow)"/><text x="275" y="286" font-size="22">g ∘ f</text>'
        return head + body + tail
    if key.startswith("graph-"):
        points = {"1": (130, 75), "2": (330, 75), "3": (330, 225), "4": (520, 75)}
        visible = ["1", "2", "3", "4"] if key == "graph-one" else ["1", "2", "3"]
        body = "".join(f'<circle cx="{points[n][0]}" cy="{points[n][1]}" r="28" fill="#fff" stroke="#37474f" stroke-width="4"/><text x="{points[n][0]-8}" y="{points[n][1]+9}" font-size="28">{n}</text>' for n in visible)
        body += '<path d="M112 55 C75 10 185 10 148 55" fill="none" stroke="#263238" stroke-width="4" marker-end="url(#arrow)"/><line x1="160" y1="75" x2="297" y2="75" stroke="#263238" stroke-width="4" marker-end="url(#arrow)"/><line x1="150" y1="98" x2="309" y2="203" stroke="#263238" stroke-width="4" marker-end="url(#arrow)"/><line x1="330" y1="105" x2="330" y2="193" stroke="#263238" stroke-width="4" marker-end="url(#arrow)"/>'
        return head + body + tail
    if key == "tree":
        coords = {"r": (320, 250), "a": (220, 150), "b": (420, 150), "c": (100, 50), "d": (220, 50), "e": (340, 50)}
        edges = [("r", "a"), ("r", "b"), ("a", "c"), ("a", "d"), ("a", "e")]
        body = "".join(f'<line x1="{coords[a][0]}" y1="{coords[a][1]}" x2="{coords[b][0]}" y2="{coords[b][1]}" stroke="#263238" stroke-width="4"/>' for a, b in edges)
        body += "".join(f'<circle cx="{x}" cy="{y}" r="25" fill="#fff" stroke="#37474f" stroke-width="4"/><text x="{x-8}" y="{y+8}" font-size="26">{name}</text>' for name, (x, y) in coords.items())
        return head + body + tail
    raise ValueError(key)


def stylesheet() -> str:
    return """@charset "UTF-8";
:root { color-scheme: light dark; }
html { font-family: Georgia, "Noto Serif", serif; line-height: 1.5; }
body { margin: 0 auto; padding: 1rem; max-width: 44rem; overflow-wrap: anywhere; }
h1, h2, h3 { font-family: "Noto Sans", Arial, sans-serif; line-height: 1.2; page-break-after: avoid; }
p { margin: 0.65rem 0; }
a { color: #4a36a8; text-decoration-thickness: 0.08em; }
img, svg { display: block; max-width: 100%; height: auto; margin: 0.5rem auto; }
figure { margin: 1rem 0; break-inside: avoid; }
figcaption { font-size: 0.92em; }
.semantic-block, .explain, .intro, .digress { border-inline-start: 0.25rem solid #7e57c2; padding: 0.1rem 0.8rem; margin: 1rem 0; }
.prob { border-inline-start-color: #00695c; }
.proof { border-inline-start-color: #455a64; }
.math-display { overflow-x: auto; overflow-y: hidden; max-width: 100%; margin: 0.8rem 0; }
math[display="block"] { display: block; max-width: 100%; }
math[display="inline"] { display: inline-block; max-width: 100%; overflow-x: auto; overflow-y: hidden; vertical-align: middle; }
.footnote { display: inline; font-size: 0.9em; }
.cover { text-align: center; }
.scope { border: 0.12rem solid #7e57c2; padding: 0.8rem; }
@media (prefers-color-scheme: dark) { a { color: #c4b5fd; } }
"""


def container_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles><rootfile full-path="EPUB/package.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>
'''


def cover_svg() -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" role="img" viewBox="0 0 1200 1600">
<title>{TITLE}</title><desc>{SUBTITLE}; wacan winates 24 saka 722 unit sumber.</desc>
<rect width="1200" height="1600" fill="#24164f"/><path d="M0 1180 Q350 900 620 1120 T1200 900 V1600 H0Z" fill="#7e57c2"/>
<text x="100" y="250" fill="#fff" font-family="serif" font-size="80">OpenLogic</text>
<text x="100" y="500" fill="#fff" font-family="sans-serif" font-size="105" font-weight="bold">Himpunan,</text>
<text x="100" y="630" fill="#fff" font-family="sans-serif" font-size="105" font-weight="bold">Relasi, lan</text>
<text x="100" y="760" fill="#fff" font-family="sans-serif" font-size="105" font-weight="bold">Fungsi</text>
<text x="100" y="880" fill="#ddd4ff" font-family="sans-serif" font-size="52">Basa Jawa · aksara Latin</text>
<text x="100" y="1420" fill="#fff" font-family="sans-serif" font-size="42">Wacan winates · 24 saka 722 unit sumber</text>
</svg>
'''


def build_nav(titles: dict[str, str]) -> str:
    used_children = {child for children in CHAPTER_CHILDREN.values() for child in children}
    items: list[str] = ['<li><a href="text/title.xhtml">Irah-irahan lan cakupan</a></li>']
    items.append(f'<li><a href="text/olp-0001.xhtml">{html.escape(titles["OLP-0001"])}</a></li>')
    for chapter, children in CHAPTER_CHILDREN.items():
        nested = "".join(f'<li><a href="text/{child.lower()}.xhtml">{html.escape(titles[child])}</a></li>' for child in children)
        items.append(f'<li><a href="text/{chapter.lower()}.xhtml">{html.escape(titles[chapter])}</a><ol>{nested}</ol></li>')
    items.append('<li><a href="text/bibliography.xhtml">Kapustakan</a></li>')
    return f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="{LANGUAGE}" xml:lang="{LANGUAGE}">
<head><meta charset="utf-8"/><title>Isine</title><link rel="stylesheet" type="text/css" href="css/book.css"/></head>
<body><nav epub:type="toc" id="toc"><h1>Isine</h1><ol>{''.join(items)}</ol></nav>
<nav epub:type="landmarks" hidden="hidden"><h2>Tandha wacan</h2><ol><li><a epub:type="cover" href="text/title.xhtml">Irah-irahan</a></li><li><a epub:type="bodymatter" href="text/olp-0004.xhtml">Wacan utama</a></li><li><a epub:type="bibliography" href="text/bibliography.xhtml">Kapustakan</a></li></ol></nav></body></html>
'''


def build_opf(commit: str, documents: list[dict], identifier: str) -> str:
    manifest = [
        '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
        '<item id="css" href="css/book.css" media-type="text/css"/>',
        '<item id="cover" href="images/cover.svg" media-type="image/svg+xml" properties="cover-image"/>',
    ]
    for key in sorted(DIAGRAM_ALT):
        manifest.append(f'<item id="img-{key}" href="images/{key}.svg" media-type="image/svg+xml"/>')
    for document in documents:
        properties = ' properties="mathml"' if document["mathml_roots"] else ""
        manifest.append(f'<item id="{document["id"]}" href="text/{document["file"]}" media-type="application/xhtml+xml"{properties}/>' )
    spine = "".join(f'<itemref idref="{document["id"]}"/>' for document in documents)
    return f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="pub-id" xml:lang="{LANGUAGE}" prefix="dcterms: http://purl.org/dc/terms/">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="pub-id">{identifier}</dc:identifier><dc:title>{TITLE}</dc:title><dc:language>{LANGUAGE}</dc:language>
<dc:creator>Open Logic Project</dc:creator><dc:contributor>Terjemahan mesin lan paninjauan dening OpenAI Codex</dc:contributor>
<dc:publisher>OpenLogic Javanese edition</dc:publisher><dc:date>2026-09-13</dc:date>
<dc:rights>Creative Commons Attribution 4.0 International; hak lan atribusi komponen asli tetep ditrapake.</dc:rights>
<dc:description>Wacan EPUB reflowable Basa Jawa aksara Latin kang ngemot pambuka lan bab Himpunan, Relasi, lan Fungsi: 24 saka 722 unit sumber. Edhisi jangkep isih digarap.</dc:description>
<dc:source>OpenLogicProject/OpenLogic@{UPSTREAM_REVISION}; translation source commit {commit}</dc:source>
<meta property="dcterms:modified">{MODIFIED}</meta><meta property="rendition:layout">reflowable</meta>
<meta property="schema:accessMode">textual</meta><meta property="schema:accessMode">visual</meta>
<meta property="schema:accessModeSufficient">textual,visual</meta>
<meta property="schema:accessibilityFeature">MathML</meta><meta property="schema:accessibilityFeature">alternativeText</meta>
<meta property="schema:accessibilityFeature">readingOrder</meta><meta property="schema:accessibilityFeature">structuralNavigation</meta><meta property="schema:accessibilityFeature">tableOfContents</meta>
<meta property="schema:accessibilityHazard">noFlashingHazard</meta><meta property="schema:accessibilityHazard">noMotionSimulationHazard</meta><meta property="schema:accessibilityHazard">noSoundHazard</meta>
<meta property="schema:accessibilitySummary">Matematika diwenehake minangka MathML asli kanthi alternatif LaTeX; kabeh diagram duwe katrangan teks; tata letak reflowable lan navigasi struktural kasedhiya.</meta>
</metadata><manifest>{''.join(manifest)}</manifest><spine>{spine}</spine></package>
'''


def write_epub(root: Path, output: Path) -> None:
    if output.exists():
        output.unlink()
    timestamp = (1980, 1, 1, 0, 0, 0)
    paths = sorted(path for path in root.rglob("*") if path.is_file())
    mimetype = root / "mimetype"
    with zipfile.ZipFile(output, "w") as archive:
        info = zipfile.ZipInfo("mimetype", timestamp)
        info.compress_type = zipfile.ZIP_STORED
        info.external_attr = 0o100644 << 16
        archive.writestr(info, mimetype.read_bytes())
        for path in paths:
            if path == mimetype:
                continue
            relative = path.relative_to(root).as_posix()
            info = zipfile.ZipInfo(relative, timestamp)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def build(args: argparse.Namespace) -> dict:
    repo = Path(__file__).resolve().parents[1]
    output_dir = Path(args.output_dir).resolve()
    if repo not in output_dir.parents:
        raise ValueError("Output directory must be inside the repository")
    if output_dir.exists():
        shutil.rmtree(output_dir)
    unpacked = output_dir / "unpacked"
    epub_root = unpacked / "EPUB"
    text_dir = epub_root / "text"
    image_dir = epub_root / "images"
    css_dir = epub_root / "css"
    meta_dir = unpacked / "META-INF"
    for directory in (text_dir, image_dir, css_dir, meta_dir):
        directory.mkdir(parents=True, exist_ok=True)

    manifest_rows = [json.loads(line) for line in (repo / "evidence" / "SOURCE_MANIFEST.jsonl").read_text(encoding="utf-8").splitlines() if line]
    manifest_by_id = {row["unit_id"]: row for row in manifest_rows}
    sources: dict[str, str] = {}
    source_records: dict[str, dict] = {}
    for unit_id in UNIT_IDS:
        expected_path = SOURCE_PATHS[unit_id]
        row = manifest_by_id[unit_id]
        if row["source_path"] != expected_path or row["source_commit"] != UPSTREAM_REVISION:
            raise ValueError(f"Source manifest drift for {unit_id}")
        path = repo / "translation" / expected_path
        payload = path.read_bytes()
        source = resolve_tokens(payload.decode("utf-8-sig"))
        source = source.replace(r"\chapter*{", r"\jvchapterstar{")
        sources[unit_id] = source
        source_records[unit_id] = {
            "unit_id": unit_id,
            "source_path": expected_path,
            "upstream_sha256": row["source_sha256"],
            "translation_bytes": len(payload),
            "translation_sha256": sha256_bytes(payload),
        }
    titles = {unit_id: discover_title(source, unit_id) for unit_id, source in sources.items()}
    labels = discover_labels(sources, titles)
    commit = current_git_commit(repo)
    identifier = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, f"https://github.com/KokunoYumeto/OpenLogic-jv-Latn-ID/releases/tag/v{VERSION}@{commit}"))

    title_body = f'''<section class="cover"><img src="../images/cover.svg" alt="Sampul {html.escape(TITLE)}"/><h1>{TITLE}</h1><p>{SUBTITLE}</p></section>
<section class="scope"><h2>Cakupan wacan iki</h2><p>Wacan iki ngemot pambuka lan telung bab jangkep: Himpunan, Relasi, lan Fungsi. Cakupane 24 saka 722 unit sumber OpenLogic. Edhisi jangkep isih digarap.</p><p>Terjemahan iki digawe mesin lan ditinjau dening sistem kang padha. Paninjauan mandiri dening panutur asli durung diklaim.</p><p>Sumber Inggris: OpenLogicProject/OpenLogic, revisi <code>{UPSTREAM_REVISION}</code>. Sumber terjemahan: commit <code>{commit}</code>.</p><p>Karya asli lan terjemahan iki nganggo <a href="https://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0</a>. Hak lan atribusi komponen asli tetep ditrapake. Terjemahan iki ora nuduhake panyengkuyung saka Open Logic Project.</p></section>'''
    title_xhtml = xhtml_document(TITLE, title_body)
    (text_dir / "title.xhtml").write_text(title_xhtml, encoding="utf-8", newline="\n")

    documents: list[dict] = [{"id": "title-page", "file": "title.xhtml", "title": TITLE, "mathml_roots": 0, "source_unit": None}]
    crosswalk_units: list[dict] = []
    context = context_db()
    for unit_id in UNIT_IDS:
        source = sources[unit_id]
        nodes, _, _ = LatexWalker(source, latex_context=context).get_latex_nodes()
        prefix = discover_prefix(source, unit_id)
        renderer = Renderer(unit_id, prefix, labels)
        body = renderer.render_flow(nodes)
        if renderer.unknown_macros or renderer.unknown_environments:
            raise ValueError(f"Unhandled LaTeX in {unit_id}: macros={sorted(renderer.unknown_macros)} environments={sorted(renderer.unknown_environments)}")
        title = renderer.title if renderer.title != unit_id else titles[unit_id]
        file_name = unit_id.lower() + ".xhtml"
        xhtml = xhtml_document(title, body, unit_id, source_records[unit_id]["translation_sha256"])
        ET.fromstring(xhtml)
        (text_dir / file_name).write_text(xhtml, encoding="utf-8", newline="\n")
        documents.append({"id": unit_id.lower(), "file": file_name, "title": title, "mathml_roots": len(renderer.math_sources), "source_unit": unit_id})
        crosswalk_units.append({
            **source_records[unit_id],
            "output": f"EPUB/text/{file_name}",
            "title": title,
            "prefix": list(prefix),
            "rendered_text_characters": len(strip_tags(body)),
            "paragraphs": body.count("<p>"),
            "environment_counts": dict(sorted(renderer.environment_counts.items())),
            "mathml_roots": len(renderer.math_sources),
            "math": renderer.math_sources,
            "images": renderer.image_count,
        })

    bibliography = xhtml_document("Kapustakan", '<h1>Kapustakan</h1><section id="bib-benacerraf1965" epub:type="bibliography"><p>Benacerraf, Paul. 1965. “What numbers could not be.” <em>The Philosophical Review</em> 74 (1): 47–73.</p></section>')
    (text_dir / "bibliography.xhtml").write_text(bibliography, encoding="utf-8", newline="\n")
    documents.append({"id": "bibliography", "file": "bibliography.xhtml", "title": "Kapustakan", "mathml_roots": 0, "source_unit": None})

    for key in sorted(DIAGRAM_ALT):
        (image_dir / f"{key}.svg").write_text(diagram_svg(key), encoding="utf-8", newline="\n")
    (image_dir / "cover.svg").write_text(cover_svg(), encoding="utf-8", newline="\n")
    (css_dir / "book.css").write_text(stylesheet(), encoding="utf-8", newline="\n")
    (unpacked / "mimetype").write_text("application/epub+zip", encoding="ascii", newline="")
    (meta_dir / "container.xml").write_text(container_xml(), encoding="utf-8", newline="\n")
    (epub_root / "nav.xhtml").write_text(build_nav(titles), encoding="utf-8", newline="\n")
    (epub_root / "package.opf").write_text(build_opf(commit, documents, identifier), encoding="utf-8", newline="\n")

    epub_path = output_dir / args.epub_name
    write_epub(unpacked, epub_path)
    package_manifest = {
        "schema": "openlogic-jv-epub-package-manifest/1",
        "epub_filename": epub_path.name,
        "entries": [
            {"path": path.relative_to(unpacked).as_posix(), "bytes": path.stat().st_size, "sha256": sha256_file(path)}
            for path in sorted(unpacked.rglob("*")) if path.is_file()
        ],
    }
    crosswalk = {
        "schema": "openlogic-jv-epub-content-crosswalk/1",
        "version": VERSION,
        "language": LANGUAGE,
        "upstream_revision": UPSTREAM_REVISION,
        "translation_source_commit": commit,
        "declared_scope": {"reader_units": 24, "corpus_units": 722, "unit_ids": UNIT_IDS},
        "units": crosswalk_units,
    }
    (output_dir / "PACKAGE_MANIFEST.json").write_bytes(canonical_json(package_manifest))
    (output_dir / "CONTENT_CROSSWALK.json").write_bytes(canonical_json(crosswalk))
    receipt = {
        "schema": SCHEMA,
        "status": "PASS",
        "version": VERSION,
        "format": "EPUB 3.3 reflowable",
        "language": LANGUAGE,
        "upstream_revision": UPSTREAM_REVISION,
        "translation_source_commit": commit,
        "modified": MODIFIED,
        "declared_scope": {"reader_units": 24, "corpus_units": 722, "supporting_source_units": 26},
        "inputs": {"source_manifest_sha256": sha256_file(repo / "evidence" / "SOURCE_MANIFEST.jsonl")},
        "outputs": {
            "epub": {"filename": epub_path.name, "bytes": epub_path.stat().st_size, "sha256": sha256_file(epub_path)},
            "package_manifest_sha256": sha256_file(output_dir / "PACKAGE_MANIFEST.json"),
            "content_crosswalk_sha256": sha256_file(output_dir / "CONTENT_CROSSWALK.json"),
        },
        "metrics": {
            "spine_documents": len(documents),
            "source_documents": len(crosswalk_units),
            "mathml_roots": sum(row["mathml_roots"] for row in crosswalk_units),
            "figures": sum(row["images"] for row in crosswalk_units),
            "xhtml_documents": len(documents) + 1,
            "svg_images": len(DIAGRAM_ALT) + 1,
        },
        "generator": {"path": "tools/build-epub.py", "sha256": sha256_file(Path(__file__))},
    }
    (output_dir / "BUILD_RECEIPT.json").write_bytes(canonical_json(receipt))
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=".build/work/epub-v020")
    parser.add_argument("--epub-name", default=f"OpenLogic-jv-Latn-ID-sets-relations-functions-v{VERSION}.epub")
    args = parser.parse_args()
    receipt = build(args)
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
