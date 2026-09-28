"""Bounded comparison view for OLP-0424 metadata and chain indexing."""


def repaired_olp0424_source(s: str) -> str:
    old = "% Chapter: frame-correspondence"
    new = "% Chapter: frame-definability"
    assert s.count(old) == 1
    s = s.replace(old, new, 1)

    old = r"\Gamma = \{!F, !A_1, !A_2, \dots\}."
    new = r"\Gamma = \{!F, !A_2, !A_3, \dots\}."
    assert s.count(old) == 1
    s = s.replace(old, new, 1)
    return s
