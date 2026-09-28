"""Bounded comparison view for quantified substitution and regularization."""


def repaired_olp0665_source(s: str) -> str:
    repairs = (
        ("$\\lexists[x][!A(x,c)]$ and of $!C$ from the open",
         "$\\lexists[x][!A(x,t)]$ and of $\\Subst{!C}{t}{c}$ from the open"),
        ("    \\[\n    \\AxiomC{}\n    \\RightLabel{$\\Subst{\\delta'}{t}{c}$}\n"
         "    \\DeduceC{$!A(a,t)$}\n    \\RightLabel{\\Intro{\\lforall}}\n"
         "    \\UnaryInfC{$\\lforall[x][!A(x,t)]$}\n    \\DisplayProof\n    \\]",
         "    \\[\n    \\AxiomC{}\n    \\RightLabel{$\\Subst{\\delta_1'}{t}{c}$}\n"
         "    \\DeduceC{$\\lexists[x][!A(x,t)]$}\n"
         "    \\AxiomC{$\\Discharge{!A(a,t)}{x}$}\n"
         "    \\RightLabel{$\\Subst{\\delta_2'}{t}{c}$}\n"
         "    \\DeduceC{$\\Subst{!C}{t}{c}$}\n"
         "    \\DischargeRule{\\Elim{\\lexists}}{x}\n"
         "    \\BinaryInfC{$\\Subst{!C}{t}{c}$}\n    \\DisplayProof\n    \\]"),
        ("neither the conclusion~$!C$ nor any open assumption",
         "neither the conclusion~$\\Subst{!C}{t}{c}$ nor any open assumption"),
        ("pick a highest eigenvariable inference,",
         "pick a highest dirty eigenvariable inference,"),
        ("regular, since it contains no eigenvariable inferences at all.",
         "regular, since any eigenvariable inference it contains is clean."),
        ("The resulting proof has $n-1$ dirty eigenvariable inferences,",
         "The resulting proof has at most $n-1$ dirty eigenvariable inferences,"),
        ("topmost eigenvariable inference is~\\Elim{\\lexists}.",
         "topmost dirty eigenvariable inference is~\\Elim{\\lexists}."),
    )
    for wrong, right in repairs:
        if r"\RightLabel{$\Subst{\delta'}{t}{c}$}" in wrong:
            assert s.count(wrong) == 2, (wrong, s.count(wrong))
            pos = s.rfind(wrong)
            s = s[:pos] + right + s[pos + len(wrong):]
            continue
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
