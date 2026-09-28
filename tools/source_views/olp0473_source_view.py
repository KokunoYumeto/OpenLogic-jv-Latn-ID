"""Bounded comparison view for the negation-rule label in the Dual proof."""


def repaired_olp0473_source(s: str) -> str:
    old = ("    \\RightLabel{\\RightR{\\lnot}}\n"
           "    \\UnaryInf$\\lnot !A, !A \\fCenter $")
    new = ("    \\RightLabel{\\LeftR{\\lnot}}\n"
           "    \\UnaryInf$\\lnot !A, !A \\fCenter $")
    assert s.count(old) == 1
    return s.replace(old, new, 1)
