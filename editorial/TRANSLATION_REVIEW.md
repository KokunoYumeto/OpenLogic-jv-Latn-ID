# Translation review log

TRANSLATION_REVIEW_LOG.jsonl is the expert-facing record of terminology and
difficult source or translation decisions for this Javanese edition. It gives
the chosen wording and constrained sense, exact locations where a searchable
term occurs, the authorities actually checked, alternatives, uncertainty, and
a concrete review question.

Coverage is partial and follows the translated corpus. The metadata record at
the start of the JSONL states the exact current range. Choices remain open to
asynchronous correction and never block translation or publication.
At the 80-file checkpoint the log contains 103 terminology or provenance
decisions and 41 difficult translation or source decisions.

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
The ten applied OLSIZ-20260904 findings and OLPL-001 through OLPL-005 have exact
machine records in evidence/SOURCE_CORRECTIONS.jsonl. The proposed OLSIZ-011 finding was retracted;
evidence/SOURCE_AUDIT_RETRACTIONS.jsonl records the exact bytes, artifact hashes,
and the fact that no corresponding correction remains in the localized body.
