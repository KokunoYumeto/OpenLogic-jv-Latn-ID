"""Bounded comparison view for the vacuous strong-induction premise."""


def repaired_olp0616_source(s: str) -> str:
    wrong = r"for all $l<0$, $P(0)$"
    right = r"for all $l<0$, $P(l)$"
    assert s.count(wrong) == 1, s.count(wrong)
    return s.replace(wrong, right, 1)
