"""Bounded quotient-world comparison view for the K finite-model proof."""


def repaired_olp0456_source(s: str) -> str:
    old = r"$\mSat{M^*}{!A}[w]$ for any filtration"
    new = r"$\mSat{M^*}{!A}[{[w]}]$ for any filtration"
    assert s.count(old) == 1
    return s.replace(old, new, 1)
