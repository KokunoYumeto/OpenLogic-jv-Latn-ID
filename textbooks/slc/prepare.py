"""Materialize a pinned OLP tree with the Javanese locale and SLC driver."""

import hashlib
import json
from pathlib import Path
import re
from shutil import copy2, copytree
from tempfile import mkdtemp

from terminology import localize


PROJECT = Path(__file__).resolve().parent
REPO = PROJECT.parents[1]


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def fingerprint(data):
    return {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


def replace_once(text, old, new, context):
    if text.count(old) != 1:
        raise ValueError(f"Expected one occurrence of {old!r} in {context}")
    return text.replace(old, new)


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def main():
    slc = load(PROJECT / "MANIFEST.json")
    published = load(REPO / "SOURCE-MANIFEST.json")
    if published["upstream_revision"] != slc["sources"]["open_logic"]["commit"]:
        raise ValueError("The source manifest names a different OLP revision")
    if len(published["units"]) != slc["sources"]["javanese_open_logic"]["locale_input_units"]:
        raise ValueError("The Javanese source manifest has a different unit inventory")
    work = PROJECT / ".build"
    work.mkdir(exist_ok=True)
    stage = Path(mkdtemp(prefix="screen-", dir=work))
    olp = stage / "olp"
    locale = olp / "locale" / slc["locale"]
    file_records = published["files"]

    def verified_source(relative):
        data = (REPO / relative).read_bytes()
        if fingerprint(data) != file_records[relative]:
            raise ValueError(f"Pinned source mismatch for {relative}")
        return data

    for relative in sorted(file_records):
        if relative.startswith("upstream/"):
            write(olp / relative.removeprefix("upstream/"), verified_source(relative))

    source_patches = {}
    for patch in load(PROJECT / "locale" / "patches.json"):
        source_patches.setdefault(patch["path"], []).append(patch)
    scope = set((PROJECT / "locale" / "scope.txt").read_text(encoding="utf-8").splitlines())
    marked = 0
    vocabulary = {}
    for unit in published["units"]:
        relative = unit["javanese"]["path"]
        data = verified_source(relative)
        text = data.decode("utf-8")
        path = relative.removeprefix("translation/")
        for patch in source_patches.pop(path, []):
            text = replace_once(text, patch["from"], patch["to"], path)
        if path in scope:
            text, replacements = localize(text, path)
            vocabulary[path] = replacements
        lines = []
        for line in text.splitlines(keepends=True):
            code, comment, note = line.partition("%")
            code, count = re.subn(r"(\\ol(?:file|chapter|part)id)(?=[ \t]*\{)",
                                  rf"\1[{slc['locale']}]", code)
            marked += count
            lines.append(code + comment + note)
        text = "".join(lines)
        write(locale / path, text.encode("utf-8"))
    if source_patches:
        raise ValueError(f"Missing localized overlay paths: {sorted(source_patches)}")
    if scope != set(vocabulary):
        raise ValueError(f"Textbook scope absent from the locale: {sorted(scope - set(vocabulary))}")

    babel = slc["babel"]
    for source_name, target_name in (
        ("jv-localization.sty", "jv-token-base.sty"),
        ("jv-complete-localization.sty", "open-logic-config.sty"),
    ):
        style = verified_source("edition/" + source_name).decode("utf-8")
        style = style.replace("{english}", "{" + babel + "}")
        style = style.replace(r"\captionsenglish", rf"\captions{babel}")
        style = style.replace(r"\extrasenglish", rf"\extras{babel}")
        if source_name == "jv-complete-localization.sty":
            style = replace_once(style, r"\input{jv-localization.sty}",
                                 rf"\input{{\olpath/locale/{slc['locale']}/jv-token-base.sty}}",
                                 source_name)
        write(locale / target_name, style.encode("utf-8"))
    copy2(PROJECT / "locale" / "open-logic-locale.sty", locale)
    copytree(PROJECT / "locale" / "photocredits", locale / "photocredits")

    # Babel supplies Javanese. cleveref has no Javanese option; the locale
    # registers the reference names and conjunctions through Babel's extras.
    master_style = olp / "sty" / "open-logic.sty"
    style = master_style.read_text(encoding="utf-8")
    style = replace_once(
        style,
        r"\RequirePackage[capitalize,nameinlink,english,\ollanguage]{cleveref}",
        r"\RequirePackage[capitalize,nameinlink,english]{cleveref}",
        master_style.name,
    )
    master_style.write_text(style, encoding="utf-8", newline="\n")

    # pdfx already sets DisplayDocTitle in the catalog for the screen class.
    # A second hyperref request writes a duplicate ViewerPreferences key.
    book_class = olp / "sty" / "open-logic-book.cls"
    class_text = book_class.read_text(encoding="utf-8")
    class_text = replace_once(class_text, "      pdfdisplaydoctitle,\n", "", book_class.name)
    book_class.write_text(class_text, encoding="utf-8", newline="\n")

    token_config = olp / "open-logic-config.sty"
    config_text = token_config.read_text(encoding="utf-8")
    for english, javanese in (
        ("is atomic: ", "atomik: "),
        ("{exercise.}", "{gladhèn.}"),
    ):
        config_text = replace_once(config_text, english, javanese, token_config.name)
    token_config.write_text(config_text, encoding="utf-8", newline="\n")

    bibliography_style = olp / "bib" / "natbib-oup.bst"
    bibliography = bibliography_style.read_text(encoding="utf-8")
    bibliography = replace_once(
        bibliography,
        'FUNCTION {bbl.and}\n{ "and"}',
        'FUNCTION {bbl.and}\n{ "lan"}',
        bibliography_style.name,
    )
    bibliography_style.write_text(bibliography, encoding="utf-8", newline="\n")

    for asset_group in ("photos", "portraits"):
        copytree(PROJECT / "assets" / asset_group, olp / "assets" / asset_group)
    book = locale / "courses" / "sets-logic-computation"
    copytree(PROJECT / "book", book)
    copy2(book / "slc-config.jv.sty", book / "slc-config.sty")
    copy2(PROJECT / "assets" / "tex" / "nowidow.sty", book)
    result = {"book": str(book), "olp": str(olp), "stage": str(stage),
              "source_units": len(published["units"]), "localized_ids": marked,
              "terminology_replacements": sum(vocabulary.values())}
    (stage / "staging.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
