"""Bounded comparison view for the induction substitution and zero case."""


def repaired_olp0615_source(s: str) -> str:
    wrong_var = r"again, now taking $1$ for~$n$"
    right_var = r"again, now taking $1$ for~$k$"
    assert s.count(wrong_var) == 1, s.count(wrong_var)
    s = s.replace(wrong_var, right_var, 1)

    marker = "(1) Is proved by inspecting a $6$-sided die."
    assert s.count(marker) == 1, s.count(marker)
    s = s.replace(marker,
                  "The zero-dice case was established above.\n" + marker, 1)
    return s
