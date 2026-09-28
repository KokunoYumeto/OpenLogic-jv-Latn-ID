"""Bounded comparison view for normalization-translation proof repairs.

The frozen English file is never modified. Each replacement asserts the
specific defect is present exactly once before QA compares the target.
"""


def repaired_olp0678_source(s: str) -> str:
    def once(wrong: str, right: str) -> None:
        nonlocal s
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)

    once(r"\Log{2i} !!{proof}s results", r"\Log{G2i} !!{proof}s results")
    once(
        "If $\\Log{G2i} \\Proves \\Gamma \\Sequent \\Delta$ then there is a normal\n"
        "\\Log{N2c}-!!{proof}~$\\delta$ of $\\Gamma' \\Sequent !C$, where the\n"
        "set~$\\Gamma'$ of labelled !!{formula}s corresponds to the\n"
        "multiset~$\\Gamma$, i.e., for every !!{formula}~$!A$, the number of\n"
        "!!{element}s of~$\\Gamma'$ of the form $x : !A$ is less than or equal\n"
        "to the multiplicity of~$!A$ (i.e., the number of copies of~$!A$)\n"
        "in~$\\Gamma$.",
        "If there is a cut-free \\Log{G2i} proof of\n"
        "$\\Gamma \\Sequent \\Delta$, there is a normal \\Log{N2i}\n"
        "proof~$\\delta$ of $\\Gamma' \\Sequent !C$. Here $!C$ is the\n"
        "formula of $\\Delta$ when nonempty, and $!C \\ident \\lfalse$\n"
        "when $\\Delta$ is empty. The set~$\\Gamma'$ corresponds to the\n"
        "multiset~$\\Gamma$: for every !!{formula}~$!A$, the number of\n"
        "!!{element}s of~$\\Gamma'$ of the form $x : !A$ does not exceed\n"
        "the multiplicity of~$!A$ (the copies of~$!A$) in~$\\Gamma$.",
    )
    once("If the \\Log{N2i}-!!{proof} we start from, this\ncan, however, be avoided.",
         "If the \\Log{N2i}-!!{proof} we start from is normal, this\ncan, however, be avoided.")
    once("of inferences in $\\delta'$ plus~$1$.",
         "of inferences in $\\delta_1$ plus~$1$.")
    once("$x:!D, \\Gamma_1 \\Sequent !A$.",
         "$!D, \\Gamma_1' \\Sequent \\Delta$.")
    once("$!D, \\Gamma_1' \\Sequent !A$ and $!E, \\Gamma_2' \\Sequent !A$. We apply",
         "$!D, \\Gamma_1' \\Sequent \\Delta$ and $!E, \\Gamma_2' \\Sequent \\Delta$. We apply")
    once(
        "If $!A \\ident \\lfalse$ we insert a\n"
        "  \\RightR{\\Weakening}, e.g,",
        "If $!A \\ident \\lfalse$ the succedent stays empty without\n"
        "  \\RightR{\\Weakening}, for example,",
    )
    once(
        "  \\UnaryInf$!D \\land !E, \\Gamma_1' \\fCenter $\n"
        "  \\RightLabel{\\RightR{\\Weakening}}\n"
        "  \\UnaryInf$!D \\land !E, \\Gamma_1' \\fCenter !A$",
        "  \\UnaryInf$!D \\land !E, \\Gamma_1' \\fCenter $",
    )
    once(
        "  Should $\\Elim{\\lor}$ not discharge $y: !D$ or $z: !E$ (i.e., these\n"
        "  aren't present in the context of the minor premises), or should~$!A$\n"
        "  happen to be $\\lfalse$, we have to add some \\LeftR{\\Weakening} and\n"
        "  \\RightR{\\Weakening}. For instance,",
        "  If $\\Elim{\\lor}$ does not discharge $y: !D$ or $z: !E$,\n"
        "  add \\LeftR{\\Weakening} as needed. If $!A \\ident \\lfalse$,\n"
        "  keep the succedent empty without \\RightR{\\Weakening}. For example,",
    )
    once(
        "  \\BinaryInf$!D \\lor !E, \\Gamma_1', \\Gamma_2' \\fCenter $\n"
        "  \\RightLabel{\\RightR{\\Weakening}}\n"
        "  \\UnaryInf$!D \\lor !E, \\Gamma_1', \\Gamma_2' \\fCenter !A$",
        "  \\BinaryInf$!D \\lor !E, \\Gamma_1', \\Gamma_2' \\fCenter $",
    )
    once(
        "  $\\Gamma_1 \\Sequent !D$ and $\\pi_2$ of $!E, \\Gamma_1' \\Sequent !A$.\n"
        "  We obtain the !!{proof}~$\\pi$ by applying \\LeftR{\\lif}:",
        "  $\\Gamma_1' \\Sequent \\Delta_D$ and $\\pi_2$ of\n"
        "  $!E, \\Gamma_2' \\Sequent \\Delta_A$. Here $\\Delta_D$ is empty if\n"
        "  $!D \\ident \\lfalse$ and is $\\{!D\\}$ otherwise; $\\Delta_A$\n"
        "  is determined the same way from $!A$. We obtain the !!{proof}~$\\pi$\n"
        "  by applying \\LeftR{\\lif}:",
    )
    once(
        "  If $!D$ and/or $!A \\ident \\lfalse$ we insert one or two\n"
        "  \\RightR{\\Weakening}, e.g,",
        "  If $!D \\ident \\lfalse$, insert \\RightR{\\Weakening} only\n"
        "  in the first premise. If $!A \\ident \\lfalse$, leave the\n"
        "  second premise and conclusion empty without right weakening, e.g,",
    )
    once(
        "  \\Deduce$!E, \\Gamma_2' \\fCenter $\n"
        "  \\RightLabel{\\RightR{\\Weakening}}\n"
        "  \\UnaryInf$!E, \\Gamma_2' \\fCenter !A$\n"
        "  \\RightLabel{\\LeftR{\\lif}}\n"
        "  \\BinaryInf$!D \\lif !E, \\Gamma_1', \\Gamma_2' \\fCenter !A$",
        "  \\Deduce$!E, \\Gamma_2' \\fCenter $\n"
        "  \\RightLabel{\\LeftR{\\lif}}\n"
        "  \\BinaryInf$!D \\lif !E, \\Gamma_1', \\Gamma_2' \\fCenter $",
    )
    once(
        "Every !!{formula} occuring in a normal \\Log{N1i} or\n"
        "\\Log{N2i}-!!{proof} is a sub-!!{formula} of the end-!!{formula} or\n"
        "end-sequent.",
        "Every !!{formula} in a normal \\Log{N1i} or \\Log{N2i} proof\n"
        "is a sub-!!{formula} of the end-!!{formula} or an undischarged\n"
        "assumption of the end-sequent.",
    )
    return s
