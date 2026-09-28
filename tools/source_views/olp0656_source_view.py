"""Bounded comparison view for topmost-cut proof-label and sequent repairs."""


def repaired_olp0656_source(s: str) -> str:
    repairs = (
        (r"In the second case, $\pi_2$ is",
         r"In the second case, $\pi_1$ is"),
        (r"\UnaryInf$\Gamma, \fCenter \Delta', !D, !D$",
         r"\UnaryInf$\Gamma \fCenter \Delta', !D, !D$"),
        (r"\Deduce$\Gamma \fCenter \Delta, !B \land !C, !C, !A$",
         r"\Deduce$\Gamma \fCenter \Delta', !B \land !C, !C, !A$"),
        (r"\BinaryInf$\Gamma \fCenter \Delta, !B \land !C, !B \land !C$",
         r"\BinaryInf$\Gamma \fCenter \Delta', !B \land !C, !B \land !C$"),
        ("\\RightSubproofLabel{$\\pi_1''$}\n\\RightLabel{\\CutCS}\n\\BinaryInf$!B, \\Gamma \\fCenter \\Delta$",
         "\\RightSubproofLabel{$\\pi_1''$}\n\\RightLabel{\\CutCS}\n\\BinaryInf$\\Gamma \\fCenter \\Delta$"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
