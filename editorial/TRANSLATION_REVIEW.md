# Translation review log

TRANSLATION_REVIEW_LOG.jsonl is the expert-facing record of terminology and
difficult source or translation decisions for this Javanese edition. It gives
the chosen wording and constrained sense, exact locations where a searchable
term occurs, the authorities actually checked, alternatives, uncertainty, and
a concrete review question.

TRANSLATION_REVIEW_INDEX.md is the readable full index, and
TRANSLATION_REVIEW_PRIORITY.md is the shorter P1/P2 expert-review view.
The machine aggregate is evidence/TRANSLATION_REVIEW_INDEX.json.
The one-row-per-tracked-occurrence projection is
evidence/TRANSLATION_REVIEW_OCCURRENCES.csv. Its printed/PDF page columns stay
blank until the next accepted reader pagination; the sealed v0.1.2 release
predates these review projections.

The canonical cross-edition contract is in `translation-decisions/`:
`DECISIONS.json` is schema validated, `TRANSLATION_DECISIONS_FULL.md` and
`PRIORITY_REVIEW.md` are its human views, and `DECISION_OCCURRENCES.csv`
binds each recorded occurrence to exact source and target line, byte, and
file-hash locators. `TRANSLATION_DECISION_QA.json` checks their agreement.

Coverage is partial and follows the translated corpus. The metadata record at
the start of the JSONL states the exact current range. Choices remain open to
asynchronous correction and never block translation or publication.
At the 97-file checkpoint the log contains 109 terminology or provenance
decisions and 48 difficult translation or source decisions.

The first terminology entries are explicitly marked retrospective backfill.
They were reconstructed from the existing term ledger and exact current files;
their rationales must not be read as claims about an unrecorded contemporaneous
thought process. Later entries say whether they were recorded contemporaneously.

A missing location is recorded as not found in the checked translated range
rather than invented. A listed canon passage establishes only the evidence role
and scope written in that record. The English OpenLogic source controls
mathematical meaning. The unavailable grammar candidate was not consulted, and
Indonesian explanatory text was not used as a semantic translation pivot.

Full canon PDFs and dictionary responses remain private research copies.
Short passage metadata and hashes are in evidence/CANON_PASSAGES.jsonl.
Source defects and their reader-facing treatment are also summarized in
ERRATA.md.
The ten applied OLSIZ-20260904 findings and OLPL-001 through OLPL-012 have exact
machine records in evidence/SOURCE_CORRECTIONS.jsonl. The proposed OLSIZ-011 finding was retracted;
evidence/SOURCE_AUDIT_RETRACTIONS.jsonl records the exact bytes, artifact hashes,
and the fact that no corresponding correction remains in the localized body.
