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
        ("  $\\pi_2$ of $\\Gamma_2' \\Sequent !B$. We obtain the !!{proof}~$\\pi$ as",
         "  $\\pi_2$ of $\\Gamma_2' \\Sequent !B$ when $!B$ is not~$\\lfalse$.\n"
         "  If $!B \\ident \\lfalse$, the inductive hypothesis yields\n"
         "  $\\Gamma_2' \\Sequent \\ $; we define $\\pi_2$\n"
         "  as a proof of $\\Gamma_2' \\Sequent !B$\n"
         "  after \\RightR{\\Weakening}.\n"
         "  We obtain the !!{proof}~$\\pi$ as"),
        ("  In the event that $!A \\ident \\lfalse$, the inductive hypothesis\n"
         "  applied to $\\delta_2$ yields !!a{proof} of $\\Gamma_2' \\Sequent \\ $,\n"
         "  from which we can obtain the !!{proof}~$\\pi$ by adding suitable\n"
         "  \\LeftR{\\Weakening} inferences and a \\RightR{\\Weakening} with~$!A$.",
         "  When $!A \\ident \\lfalse$, $\\pi_2$ as defined above\n"
         "  proves $\\Gamma_2' \\Sequent !B$.\n"
         "  The displayed construction gives the !!{proof}~$\\pi$ with~$!A$ on the right.\n"
         "  A further \\Cut against the false-left axiom gives an empty succedent."),
        ("  \\Deduce$x: \\lnot !A, \\Gamma' \\fCenter $",
         "  \\Deduce$\\lnot !A, \\Gamma' \\fCenter $"),
        ("  \\BinaryInf$\\Gamma' \\fCenter !A$\n"
         "  \\DisplayProof\n"
         "  \\]\n"
         "\\end{enumerate}",
         "  \\BinaryInf$\\Gamma' \\fCenter !A$\n"
         "  \\DisplayProof\n"
         "  \\]\n"
         "  If $!A \\ident \\lfalse$, this construction yields\n"
         "  $\\Gamma' \\Sequent \\lfalse$; another \\Cut with the axiom\n"
         "  $\\lfalse \\Sequent \\ $ gives $\\Gamma' \\Sequent \\ $.\n"
         "\\end{enumerate}"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
