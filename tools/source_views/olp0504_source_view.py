"""Bounded comparison for the assumption macro and induction-hypothesis wording."""


def repaired_olp0504_source(s: str) -> str:
    repairs = (
        (r"\mSat{M}{\Gamma}{!A_n}[w]", r"\mSat{M}{!A_n}[w]"),
        ("holds vacuously. So the claim holds for all !!{derivation}s of",
         "holds vacuously. For the induction step, assume the claim holds for all !!{derivation}s of"),
    )
    for old, new in repairs:
        assert s.count(old) == 1
        s = s.replace(old, new, 1)
    return s
