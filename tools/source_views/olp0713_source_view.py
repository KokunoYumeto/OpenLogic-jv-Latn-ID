"""Repair G3 axiom status and complete the quantified-rule simulations."""
def repaired_olp0713_source(s: str) -> str:
    repairs = (
        ("arbitrary, not just atomic~$!A$ are allowed.", "arbitrary, not just atomic~$!A$ are not allowed."),
        (r"\UnaryInf$\Gamma \fCenter \Delta, , !A \lor !B, !A \lor !B$", r"\UnaryInf$\Gamma \fCenter \Delta, !A \lor !B, !A \lor !B$"),
        ("The exceptions are the rules\n  \\LeftR{\\land} and \\RightR{\\lor}, which differ", "The exceptions are the rules\n  \\LeftR{\\land}, \\RightR{\\lor}, \\LeftR{\\lforall}, and\n  \\RightR{\\lexists}, which differ"),
        (r"\olref[inv]{prop:G3c-cont-adm}." + "\n\\end{proof}", r"\olref[inv]{prop:G3c-cont-adm}." + "\n" + r"  For \LeftR{\lforall} and \RightR{\lexists} in \Log{G1c}, first use" + "\n" + r"  admissible \LeftR{\Weakening} or \RightR{\Weakening} to add the" + "\n" + r"  retained quantified principal formula, then apply the corresponding \Log{G3c} rule." + "\n\\end{proof}"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, wrong
        s = s.replace(wrong, right, 1)
    ending = "  \\]\n\\end{proof}"
    assert s.count(ending) == 1
    extra = r"""  \]
  The retained principal formulas in \LeftR{\lforall} and \RightR{\lexists}
  are handled in \Log{G1c} by the corresponding rule followed by contraction:
  \[
  \Axiom$!A(t), \lforall[x][!A(x)], \Gamma \fCenter \Delta$
  \RightLabel{\LeftR{\lforall}}
  \UnaryInf$\lforall[x][!A(x)], \lforall[x][!A(x)], \Gamma \fCenter \Delta$
  \RightLabel{\LeftR{\Contraction}}
  \UnaryInf$\lforall[x][!A(x)], \Gamma \fCenter \Delta$
  \DisplayProof
  \qquad
  \Axiom$\Gamma \fCenter \Delta, \lexists[x][!A(x)], !A(t)$
  \RightLabel{\RightR{\lexists}}
  \UnaryInf$\Gamma \fCenter \Delta, \lexists[x][!A(x)], \lexists[x][!A(x)]$
  \RightLabel{\RightR{\Contraction}}
  \UnaryInf$\Gamma \fCenter \Delta, \lexists[x][!A(x)]$
  \DisplayProof
  \]
\end{proof}"""
    return s.replace(ending, extra, 1)
