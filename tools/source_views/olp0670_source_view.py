"""Bounded comparison view for the G2i-to-N2i proof defects."""


def repaired_olp0670_source(s: str) -> str:
    repairs = (
        ("and $\\Delta = \\{!A\\}$ otherwise, and $\\Gamma'$ corresponds",
         "and $\\Delta = \\{!A\\}$ otherwise, with C that sole formula, and $\\Gamma'$ corresponds"),
        ("  \\Log{G2ci}, then there is", "  \\Log{G2i} + \\Cut, then there is"),
        ("the premises of that rule in~\\Log{N2c}.",
         "the premises of that rule in~\\Log{N2i}."),
        ("    \\Deduce$\\Gamma \\fCenter \\Delta$\n    \\RightLabel{\\RightR{\\Weakening}}",
         "    \\Deduce$\\Gamma \\fCenter \\Delta$\n    \\RightLabel{\\LeftR{\\Weakening}}"),
        ("The induction hypothesis applied to $\\pi_1$ yields !!a{proof}\n    of~$\\Pi, \\Gamma' \\Sequent !C$",
         "The induction hypothesis applied to $\\pi_1$ yields !!a{proof}~$\\delta_1$\n    of~$\\Pi, \\Gamma' \\Sequent !C$"),
        ("We can take $\\delta_1$\n    to be $\\delta$ plus an application of \\Intro{\\lif}.",
         "We can extend $\\delta_1$\n    to obtain $\\delta$ by an application of \\Intro{\\lif}."),
        ("$\\Gamma_2' \\Sequent !A$. By", "$\\Gamma_2' \\Sequent !B$. By"),
        ("relabelling all formulas and discharge labels in~$\\pi_2$",
         "relabelling all formulas and discharge labels in~$\\delta_2$"),
        ("In the latter case, we can take $\\delta_1$\n    to be $\\delta$.",
         "In the latter case, $\\delta_1$\n    can serve as $\\delta$."),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)

    start = s.index("    \\item If $R$ is \\LeftR{\\Contraction}")
    end = s.index("    \\item If $R$ is $\\RightR{\\lif}$", start)
    block = s[start:end]
    marker = "If $\\Pi = \\{x : !A, y:!A\\}$"
    assert block.count(marker) == 1
    before, after = block.split(marker, 1)
    assert after.count("$\\pi_1$") == 4, after.count("$\\pi_1$")
    after = after.replace("$\\pi_1$", "$\\delta_1$")
    s = s[:start] + before + marker + after + s[end:]

    start = s.index("    \\item If $R$ is \\LeftR{\\lif}")
    end = s.index("    \\item If $R$ is \\RightR{\\land}", start)
    block = s[start:end]
    wrong = "formulas and discharge labels in~$\\pi_1$"
    assert block.count(wrong) == 1
    block = block.replace(wrong, "formulas and discharge labels in~$\\delta_1$", 1)
    s = s[:start] + block + s[end:]
    return s
