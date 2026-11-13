"""Embed the pinned SLC modules without expanding their TeX bodies."""
from argparse import ArgumentParser
from pathlib import Path, PurePosixPath
import re


IMPORT = re.compile(r"\\olimport(\*)?[ \t]*(?:\[([^][]*)\][ \t]*)?\{([^{}\n]+)\}(?:\[([^][]*)\])?")
ABOUT = r"\olpath/locale/\ollangid/content/open-logic-about"
BOOK = Path("olp/locale/jv/courses/sets-logic-computation")
SUMMARIES = (1, 2, 3, 4, 6, 7, 8, 10, 11, 12, 14, 15)
MODULE_NAME = "slc-module-{:03d}.tex"


def retarget_imports(text, relative, modules):
    def convert(match):
        star, directory, name, sectioning = match.groups()
        if name == ABOUT:
            target = "content/open-logic-about.tex"
        else:
            if any("\\" in part for part in (directory or "", name)):
                raise ValueError((relative, match[0]))
            base = PurePosixPath("content") if star and directory else PurePosixPath(relative).parent
            target = (base / (directory or "") / name).as_posix()
            if not target.endswith(".tex"):
                target += ".tex"
        if target not in modules:
            # The pinned SLC tags suppress these upstream branches.
            return r"\slcMissingImport{" + target + "}"
        return r"\slcEmbeddedImport{" + modules[target] + "}" + (
            "[" + sectioning + "]" if sectioning else ""
        )

    lines = []
    for line in text.splitlines(keepends=True):
        parts = re.split(r"(?<!\\)%", line, maxsplit=1)
        lines.append(IMPORT.sub(convert, parts[0]) + ("%" + parts[1] if len(parts) > 1 else ""))
    return "".join(lines)


def embed(name, text):
    if r"\end{filecontents" in text:
        raise ValueError(f"Nested filecontents in {name}")
    return f"\\begin{{filecontents*}}[overwrite]{{{name}}}\n{text.rstrip()}\n\\end{{filecontents*}}\n"


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("tree", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    project = Path(__file__).resolve().parent
    scope = (project / "locale/scope.txt").read_text(encoding="utf-8").splitlines()
    modules = {path: MODULE_NAME.format(index) for index, path in enumerate(scope, 1)}
    book = args.tree / BOOK
    locale = book.parent.parent

    def read(path):
        return path.read_text(encoding="utf-8")

    sections = [
        "% Himpunan, Logika, Komputasi — LaTeX kumulatif.\n"
        "% Disusun dening Richard Zach saka karya Open Logic Project. Teks CC BY 4.0.\n"
        "% Terjemahan diprodhuksi AI OpenAI Codex, GPT-6.1 Sol (Ultra).\n"
        "% Pandhuan ngasilake PDF lan lisensi komponen ana ing arsip sumber.\n"
    ]
    for relative, filename in modules.items():
        sections.append("% " + relative + "\n" + embed(filename, retarget_imports(read(locale / relative), relative, modules)))
    extras = ("preface", "glossary", "cover-text", *(f"summary-{n}" for n in SUMMARIES))
    for name in extras:
        sections.append(embed(f"slc-embedded-{name}.tex", read(book / f"include/{name}.tex")))
    metadata = read(book / "slc-metadata.tex").replace("include/cover-text", "slc-embedded-cover-text")
    sections.append(embed("slc-embedded-metadata.tex", metadata))
    main_book = retarget_imports(read(book / "slc.tex"), "", modules)
    main_book = main_book.replace("include/preface", "slc-embedded-preface").replace(
        r"include/summary-\thechapter", r"slc-embedded-summary-\thechapter"
    )
    sections.append(embed("slc-embedded-book.tex", main_book))
    driver = read(book / "slc-screen.tex").replace("include/glossary", "slc-embedded-glossary")
    driver = driver.replace(r"\input{slc-metadata}", r"\input{slc-embedded-metadata}")
    driver = driver.replace(r"\input{slc}", r"\input{slc-embedded-book}")
    dispatch = r"""\makeatletter
\NewDocumentCommand \slcEmbeddedImport {m O{section}}{%
  \begingroup
  \def\ol@sectioncs{#2}%
  \def\olfilename{#1}%
  \subfile{#1}%
  \endgroup}
\NewDocumentCommand \slcMissingImport {m}{%
  \PackageError{slc-jv}{Unexpected active import #1}{}}
\makeatother
"""
    anchor = r"\begin{document}"
    if driver.count(anchor) != 1:
        raise ValueError("Unexpected driver structure")
    sections.append(driver.replace(anchor, dispatch + anchor))
    args.output.write_text("\n".join(sections), encoding="utf-8", newline="\n")
    print(f"{len(modules)} embedded modules; {len(SUMMARIES)} summaries")


if __name__ == "__main__":
    main()
