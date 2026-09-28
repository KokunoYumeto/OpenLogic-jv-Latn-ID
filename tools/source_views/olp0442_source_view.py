"""Bounded comparison view for the misplaced premise-set symbol in OLP-0442."""


def repaired_olp0442_source(s: str) -> str:
    old = "$\\Sigma\n\\Proves/[\\Sigma] \\lnot !A$"
    new = "$\\Proves/[\\Sigma] \\lnot !A$"
    assert s.count(old) == 1
    return s.replace(old, new, 1)
