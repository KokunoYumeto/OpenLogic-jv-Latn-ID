"""Exact bounded repairs to worked sequent proofs and formula depth."""
def repaired_olp0702_source(s: str) -> str:
    repairs = (
        (r"$\Gamma = \{!C \lif (!D \lif !E)\}$", r"$\Gamma = \{(!C \land !D) \lif !E\}$", 1),
        (r"\RightLabel{\RightR{\lif}}" + "\n" + r"\BinaryInf$ !D, !C, (!C \land !D) \lif !E \fCenter !E$",
         r"\RightLabel{\LeftR{\lif}}" + "\n" + r"\BinaryInf$ !D, !C, (!C \land !D) \lif !E \fCenter !E$", 1),
        (r"\UnaryInf$!D, !C \fCenter !E, !C$" + "\n\\]", r"\UnaryInf$!D, !C \fCenter !E, !C$" + "\n\\DisplayProof\n\\]", 1),
        (r"\UnaryInf$!C, !E \fCenter !C$", r"\UnaryInf$!C, !E \fCenter !E$", 1),
        (r"\[\Log{G1c} \Proves (!C \land !D) \lif !E \fCenter !C \lif (!D \lif", r"\[\Log{G3c} \Proves (!C \land !D) \lif !E \fCenter !C \lif (!D \lif", 1),
        (r"\lforall[x][A]", r"\lforall[x][!B]", 1),
        (r"\lexists[x][A]", r"\lexists[x][!B]", 1),
        (r"\lforall[x][A(x)]", r"\lforall[x][!B(x)]", 1),
        (r"\lforall[x][B(x)]", r"\lforall[x][!B(x)]", 4),
        (r"\lexists[x][B(x)]", r"\lexists[x][!B(x)]", 2),
        (r"\depth{B(c)}", r"\depth{!B(c)}", 1),
        (r"\BinaryInf$!B \land !C \fCenter !B \land !C$" + "\n  " + r"\RightLabel{\LeftR{\Contraction}}" + "\n  " + r"\UnaryInf$!B \land !C \fCenter !B$",
         r"\BinaryInf$!B \land !C, !B \land !C \fCenter !B \land !C$" + "\n  " + r"\RightLabel{\LeftR{\Contraction}}" + "\n  " + r"\UnaryInf$!B \land !C \fCenter !B \land !C$", 1),
        (r"for all $D!$", r"for all $!D$", 1),
        (r"$\Pi = !B, \Lambda$", r"$\Pi = !B, \Gamma$", 1),
        ("in any rule, the depth of\nthe principal !!{formula} is always greater than the depth of the\nactive !!{formula}s",
         "in every logical rule, the depth of\nthe principal !!{formula} is greater than the depth of its proper\ncomponents, including quantifier instances; unchanged retained principal\nformulas are excluded from these decomposed active !!{formula}s", 1),
        ("they are not quite axioms yet", "whether they are axioms depends on the system", 1),
        ("In \\Log{G3c}, axioms are sequents of the form", "In \\Log{G3c}, identity axioms are sequents of the form", 1),
        ("it is only \\emph{really} an axiom if", "it is guaranteed by this shared formula to be \\emph{really} an axiom if", 1),
        ("Our proof fragment is only a complete proof in \\Log{G3c} if", "Our proof fragment is certainly a complete proof in \\Log{G3c} if", 1),
    )
    for wrong, right, count in repairs:
        assert s.count(wrong) == count, (wrong, s.count(wrong))
        s = s.replace(wrong, right)
    return s
