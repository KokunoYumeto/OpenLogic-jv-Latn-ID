"""Bounded comparison view for two notation defects in OLP-0423."""


def repaired_olp0423_source(s: str) -> str:
    old = r"$\mSat{M}{\Box !A}$ and $\mSat/{M}{\Diamond !A}[w]$"
    new = r"$\mSat{M}{\Box !A}[w]$ and $\mSat/{M}{\Diamond !A}[w]$"
    assert s.count(old) == 1
    s = s.replace(old, new, 1)

    old = r"$V(q) = \emptyset)$"
    new = r"$V(q) = \emptyset$)"
    assert s.count(old) == 1
    s = s.replace(old, new, 1)
    return s
