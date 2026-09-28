"""Bounded comparison view for the mislabeled S5 tableau example."""


def repaired_olp0465_source(s: str) -> str:
    old = ("  We give a closed tableau that shows $\\Log{S5} \\Proves \\Ax{5}$, i.e.,\n"
           "  $\\Box!A \\lif \\Box\\Diamond!A$.")
    new = ("  We give a closed tableau that shows\n"
           "  $\\Log{S5} \\Proves \\Box!A \\lif \\Box\\Diamond!A$.")
    assert s.count(old) == 1
    return s.replace(old, new, 1)
