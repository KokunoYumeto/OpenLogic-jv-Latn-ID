"""Repair G3i's disjunction grammar, separator, minimal comparison and table identity."""
def repaired_olp0708_source(s: str) -> str:
    wrong_disjunction = r"""\Axiom$\Gamma \fCenter !A, !B$
\RightLabel{\RightR{\lor}}
\UnaryInf$ \Gamma \fCenter !A \lor !B$
\DisplayProof"""
    right_disjunction = r"""\begin{tabular}[t]{@{}r@{}}
\Axiom$\Gamma \fCenter !A$
\RightLabel{\RightR{\lor}}
\UnaryInf$ \Gamma \fCenter !A \lor !B$
\DisplayProof
\\[3ex]
\Axiom$\Gamma \fCenter !B$
\RightLabel{\RightR{\lor}}
\UnaryInf$ \Gamma \fCenter !A \lor !B$
\DisplayProof
\end{tabular}"""
    repairs = (
        (wrong_disjunction, right_disjunction),
        (r"\Axiom$ !A(t), \lforall[x][!A(x)]\Gamma \fCenter \Delta$", r"\Axiom$ !A(t), \lforall[x][!A(x)], \Gamma \fCenter \Delta$"),
        (r"\Log{G1m} is \Log{G1i}", r"\Log{G3m} is \Log{G3i}"),
        (r"\ollabel{tab:G3c}", r"\ollabel{tab:G3i}"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, wrong
        s = s.replace(wrong, right, 1)
    return s
