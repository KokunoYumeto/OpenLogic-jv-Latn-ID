# Build the Javanese reader

The current reader contains the introduction and complete sets, relations, and
functions chapters. Its driver is edition/jv-sets.tex. Other translated sources
are continuing work toward the full 722-file edition and are not automatically
included in this reader.

On Windows, install PowerShell and a TeX distribution providing pdfLaTeX,
BibTeX, memoir, mathpazo, microtype, TikZ, and the packages required by the pinned
OpenLogic style. Put pdflatex and bibtex on PATH, then run from this directory:

    powershell -NoProfile -File tools/build-reader.ps1

The output is .build/work/tex-sets/jv-sets.pdf. The script acquires the
machine-wide Global\InterlanguageTeXSlotV1 mutex before any TeX or BibTeX process,
captures each process tree before it runs, holds the mutex across all passes
and immediate log checks, and releases it in a finally path. An occupied slot
returns without launching an engine. Each captured process tree has a
180-second limit. Shell escape and automatic package installation are disabled.

To replay from a fresh directory and compare bytes, pass a new BuildName and the
absolute path of the first PDF as ReferencePdf. ReferencePdf must lie inside
this checkout's .build/work directory. The comparison runs while the same
mutex is held. Do not run concurrent or unguarded TeX jobs.

The original English files under upstream/ are pinned and unmodified.
Translation files preserve source identifiers, formula notation and import
order. The reader applies Javanese captions and token forms; editorial/ERRATA.md
and edition/jv-errata.tex distinguish source corrections from aligned text.

Evidence under evidence/ records exact source and translation hashes, paragraph
alignment, short canon passages, terminology decisions, same-author semantic
reviews, applied source corrections, and audit retractions. Canon original PDFs and full dictionary responses are private
consultation copies and are not part of this repository. Original book titles,
personal names used for scholarly attribution, citations, URLs, source-code
identifiers and mathematical notation are intentional language exceptions.
Source English diaeresis and discretionary hyphenation commands inside the
translated words naive and anti-symmetric have explicit lexical-typesetting
exceptions in the structural audit.
The pp. citation locator in OLP-0037 is localized as kaca while retaining its
page numbers and citation key. Paragraph and segment-hash analysis normalizes
CRLF/LF line endings; whole-file hashes always describe the original bytes.

Run `python tools/qa-batch.py` from the repository root to replay the structural
and alignment evidence against the checked-out bytes. Confirmed source repairs
are normalized only at their exact asserted source strings. In OLP-0048 this
includes the complete `\equivrep{f}{}\neq 0_\Rat` expression before command
sequence comparison, matching its audited `0_\Real` target correction.

The build produces a searchable visual PDF, without a claim of PDF/UA tagging,
screen-reader certification, synthesized audio, or native-language review.
