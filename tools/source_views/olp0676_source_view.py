"""Bounded comparison view for reduction-conversion source defects."""


def repaired_olp0676_source(s: str) -> str:
    repairs = (
        ("$\\delta_2$, $\\delta_3$, or\n$\\delta_4$, or entirely outside",
         "$\\delta_2$ or $\\delta_3$, or entirely outside"),
        ("If $B^x$ was a minor premise", "If $!B^x$ was a minor premise"),
        ("\\AxiomC{$\\Discharge{!C}{x}$}\n"
         "\\RightLabel{$\\delta_4$}\n"
         "\\DeduceC{$!D$}\n"
         "\\RightLabel{\\Elim{\\lor}}\n",
         "\\AxiomC{$\\Discharge{!C}{y}$}\n"
         "\\RightLabel{$\\delta_4$}\n"
         "\\DeduceC{$!D$}\n"
         "\\DischargeRule{\\Elim{\\lor}}{x\\,y}\n"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
