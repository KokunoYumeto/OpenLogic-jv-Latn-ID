"""Bounded comparison view for the temporal future-operator typo."""


def repaired_olp0478_source(s: str) -> str:
    old = r"$F !A$"
    new = r"$\Ftemp !A$"
    assert s.count(old) == 1
    return s.replace(old, new, 1)
