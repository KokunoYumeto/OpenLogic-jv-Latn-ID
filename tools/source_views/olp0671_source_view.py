"""Bounded comparison view for N2-to-G2 translation corrections."""


def repaired_olp0671_source(s: str) -> str:
    repairs = (
        ("$\\Log{G2c}\\ (\\Log{N2i}) + \\Cut \\Proves \\Gamma'",
         "$\\Log{G2c}\\ (\\Log{G2i}) + \\Cut \\Proves \\Gamma'"),
        ("  \\Sequent !C$, from which we obtain $\\pi$ by applying\n"
         "  \\LeftR{\\Weakening} with~$!B$, and then~\\RightR{\\lif}.",
         "  \\Sequent !C$ when C is not false; if it is false the succedent is empty "
         "and we apply \\RightR{\\Weakening} first. We then obtain $\\pi$ by applying\n"
         "  \\LeftR{\\Weakening} with~$!B$, and then~\\RightR{\\lif}."),
        ("  In the event that $!A \\ident \\lfalse$, the inductive hypothesis\n"
         "  applied to $\\delta_2$ yields !!a{proof} of $\\Gamma_2' \\Sequent \\ $,\n"
         "  from which we can obtain the !!{proof}~$\\pi$ by adding suitable\n"
         "  \\LeftR{\\Weakening} inferences and a \\RightR{\\Weakening} with~$!A$.",
         "  When $!A \\ident \\lfalse$, the inductive hypothesis\n"
         "  applied to $\\delta_2$ still yields !!a{proof} of $\\Gamma_2' \\Sequent !B$.\n"
         "  The displayed construction gives the !!{proof}~$\\pi$ with~$!A$ on the right.\n"
         "  A further \\Cut against the false-left axiom gives an empty succedent."),
        ("  \\Deduce$x: \\lnot !A, \\Gamma' \\fCenter $",
         "  \\Deduce$\\lnot !A, \\Gamma' \\fCenter $"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
