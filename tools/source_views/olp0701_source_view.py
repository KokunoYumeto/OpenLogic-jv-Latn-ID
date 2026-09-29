"""Seven bounded correction groups for invertibility and contraction proofs."""
def repaired_olp0701_source(s: str) -> str:
    repairs = (
        (r"$\Proves[h_i] S_i$ for $i = 1$", r"$\Proves S_i$ for $i = 1$"),
        (r"whenever $\Proves_n S$ then $\Proves[n] S_i$", r"whenever $\Proves_h S$ then $\Proves[h] S_i$"),
        ("for any rule~$R$ of~\\Log{G3c}", "for any of the propositional rules~$R$ of~\\Log{G3c}"),
        ("In \\Log{G3c}, axioms are of the form", "In \\Log{G3c}, identity axioms are of the form"),
        ("and~$\\Delta$. But then $!A, !B, \\Gamma", "and~$\\Delta$, or falsity occurs in the antecedent context. But then $!A, !B, \\Gamma"),
        ("applies if the end-sequent is $!A, !A, \\Gamma \\Sequent\n\\Delta$.", "applies if the end-sequent is $!A, !A, \\Gamma \\Sequent\n\\Delta$. Falsity in the antecedent also survives contraction, including\nwhen it is the contracted formula on the left."),
        ("either some atomic~$!C$ is !!a{element}", "in the identity case, either some atomic~$!C$ is !!a{element}"),
        (r"$!A \land !B, \Gamma' \Sequent \Delta, !C$ and $!A \land !B, \Gamma'," + "\n!D \\Sequent \\Delta$",
         r"$!A, !B, \Gamma' \Sequent \Delta, !C$ and $!A, !B, \Gamma'," + "\n!D \\Sequent \\Delta$"),
        (r"\RightLabel{\RightR{\lexists}}" + "\n" + r"\UnaryInf$\Gamma \fCenter \Delta, \lforall[x][!B(x)], \lforall[x][!B(x)]$",
         r"\RightLabel{\RightR{\lforall}}" + "\n" + r"\UnaryInf$\Gamma \fCenter \Delta, \lforall[x][!B(x)], \lforall[x][!B(x)]$"),
        ("!B$. (Note that no inversion lemma", "!B(t)$. (Note that no inversion lemma"),
        (r"\Deduce$\Gamma \fCenter \Delta,  \lexists[x][!B(x)], !B$", r"\Deduce$\Gamma \fCenter \Delta,  \lexists[x][!B(x)], !B(t)$"),
        ("We show (1) and leave (2) as an exercise. The argument is similar to", "We show (1) and leave (2) as an exercise. The same identity and falsity\n  axiom base cases apply. First rename eigenparameters within their proof\n  subtrees fresh for the chosen constant. The argument is similar to"),
        ("Let $c$ be !!a{constant} that\ndoes not appear in $\\Delta$", "Take $c$ to be !!a{constant} satisfying the full freshness condition above;\nin particular, it does not appear in $\\Delta$"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, wrong
        s = s.replace(wrong, right, 1)
    return s
