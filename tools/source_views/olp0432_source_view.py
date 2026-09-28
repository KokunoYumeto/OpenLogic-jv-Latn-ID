"""Bounded comparison view for OLP-0432's missing formula metavariable mark."""


def repaired_olp0432_source(s: str) -> str:
    old = r"\Subst{!C}{B}{q}"
    new = r"\Subst{!C}{!B}{q}"
    assert s.count(old) == 1
    s = s.replace(old, new, 1)
    old = "``$!A$ for $!B$''"
    new = "``$!B$ for $!A$''"
    assert s.count(old) == 2
    return s.replace(old, new)
