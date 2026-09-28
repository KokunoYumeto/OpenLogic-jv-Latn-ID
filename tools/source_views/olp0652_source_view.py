"""Bounded comparison view for the many-valued exercise cross-reference."""


def repaired_olp0652_source(s: str) -> str:
    wrong = r"\olref[fol][seq][ptn]{prop:incons}"
    right = r"\olref[mvl][seq][prf]{prop:incons}"
    assert s.count(wrong) == 1
    return s.replace(wrong, right, 1)
