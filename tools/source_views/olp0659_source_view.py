"""Bounded comparison view for broken proof token and CutCS diagram label."""


def repaired_olp0659_source(s: str) -> str:
    repairs = (
        ("we take a part of !!\na{proof}",
         "we take a part of !!a{proof}"),
        ("\\Axiom$!A, \\Gamma \\fCenter \\Delta$\n\\RightLabel{\\Cut}\n\\BinaryInf$\\Gamma \\fCenter \\Delta$",
         "\\Axiom$!A, \\Gamma \\fCenter \\Delta$\n\\RightLabel{\\CutCS}\n\\BinaryInf$\\Gamma \\fCenter \\Delta$"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
