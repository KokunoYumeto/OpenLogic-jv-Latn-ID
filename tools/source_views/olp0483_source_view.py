"""Bounded comparison view for Hintikka's bibliographic name."""


def repaired_olp0483_source(s: str) -> str:
    old = "Jaako Hintikka's"
    new = "Jaakko Hintikka's"
    assert s.count(old) == 1
    return s.replace(old, new, 1)
