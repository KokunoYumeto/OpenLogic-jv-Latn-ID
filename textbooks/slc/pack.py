"""Package the exact recorder inputs of the Javanese SLC screen reader."""
from argparse import ArgumentParser
from hashlib import sha256
import json
from pathlib import Path
import subprocess
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from assemble import BOOK


def recorded_inputs(stage):
    book = stage / BOOK
    recorder = (book / "slc-screen.fls").read_text(encoding="utf-8")
    outputs = {(book / line[7:]).resolve() for line in recorder.splitlines() if line.startswith("OUTPUT ")}
    outputs.update(book / f"slc-screen.{ext}" for ext in ("bbl", "gls"))
    files = {}
    for line in recorder.splitlines():
        if not line.startswith("INPUT "):
            continue
        path = (book / line[6:]).resolve()
        if path.is_relative_to(stage) and path not in outputs and path.is_file():
            files[path.relative_to(stage).as_posix()] = path.read_bytes()
    return files


def zip_files(path, files):
    with ZipFile(path, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(files.items()):
            info = ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data, compress_type=ZIP_DEFLATED, compresslevel=9)
    with ZipFile(path) as archive:
        assert archive.testzip() is None and set(archive.namelist()) == set(files)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("stage", type=Path)
    args = parser.parse_args()
    stage = args.stage.resolve()
    project = Path(__file__).resolve().parent
    receipt = json.loads((stage / "build.json").read_bytes())
    if receipt["status"] != "complete" or receipt["inventory"]["imported_modules"] != 176:
        raise ValueError("Expected the accepted modular screen build")
    subprocess.run(["python", str(project / "assemble.py"), str(stage), str(project / "slc-screen-jv.tex")], check=True)
    files = recorded_inputs(stage)

    def add(path, name):
        files[name] = path.read_bytes()

    def add_project(path, name=None):
        add(project / path, path if name is None else name)

    for name in ("LICENSE-SLC.md", "MANIFEST.json", "BUILD.md", "build.ps1", "check-build.py", "locale/scope.txt", "slc-screen-jv.tex"):
        add_project(name)
    add(project.parents[1] / "tools/WindowsTexJob.cs", "WindowsTexJob.cs")
    add(stage / "olp/LICENSE.md", "olp/LICENSE.md")
    add_project("assets/portraits/LICENSE.md", "olp/assets/portraits/LICENSE.md")
    add_project("assets/photos/README.md", "olp/assets/photos/README.md")
    for path in (project / "assets/photos").glob("*/*-credit.tex"):
        add(path, "olp/" + path.relative_to(project).as_posix())
    for name in ("README", "nowidow.dtx", "nowidow.ins"):
        add_project("assets/tex/" + name)
    add(stage / BOOK / "slc-screen.xmpdata", (BOOK / "slc-screen.xmpdata").as_posix())
    # BibTeX dependencies are inputs to the build, though pdfLaTeX does not read them.
    for name in ("bib/open-logic.bib", "bib/natbib-oup.bst"):
        add(stage / "olp" / name, "olp/" + name)
    # The two modes have the same XMP metadata.
    files[(BOOK / "slc-screen-jv.xmpdata").as_posix()] = files[(BOOK / "slc-screen.xmpdata").as_posix()]
    files[(BOOK / "slc-screen-jv.tex").as_posix()] = files["slc-screen-jv.tex"]
    if any(name.endswith((".aux", ".bbl", ".fls", ".glo", ".gls", ".log", ".out", ".toc")) for name in files):
        raise ValueError("A generated TeX intermediate entered the source archive")
    files["SOURCE-SHA256SUMS.txt"] = "".join(
        f"{sha256(data).hexdigest()}  {name}\n" for name, data in sorted(files.items())
    ).encode("utf-8")
    archive = project / "slc-source-jv.zip"
    zip_files(archive, files)
    outputs = ("slc-screen-jv.pdf", "slc-screen-jv.tex", archive.name)
    checksums = "".join(f"{sha256((project / name).read_bytes()).hexdigest()}  {name}\n" for name in outputs)
    (project / "SHA256SUMS.txt").write_text(checksums, encoding="ascii", newline="\n")
    print(f"{len(files)} files in {archive.name}")


if __name__ == "__main__":
    main()
