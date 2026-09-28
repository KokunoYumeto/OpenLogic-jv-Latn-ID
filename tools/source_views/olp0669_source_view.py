"""Bounded comparison view for the N1/N2 sequent correspondence."""


def repaired_olp0669_source(s: str) -> str:
    repairs = (
        ("!!^a{proof}~$\\delta$ in \\Log{G1c} or \\Log{G1i}",
         "!!^a{proof}~$\\delta$ in \\Log{N1c} or \\Log{N1i}"),
        ("\\Deduce$x:B, \\Gamma \\fCenter !C$",
         "\\Deduce$x:!B, \\Gamma \\fCenter !C$"),
        ("  assumption of~$\\delta'$; in the second case it is not.",
         "  assumption in the upper subproof of~$\\delta'$; in the second case it is not."),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
