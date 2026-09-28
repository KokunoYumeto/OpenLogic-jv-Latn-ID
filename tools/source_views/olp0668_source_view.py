"""Bounded comparison view for four defects in the N1 proof rules."""


def repaired_olp0668_source(s: str) -> str:
    repairs = (
        ("are finite trees of sequents\nthat are inductively generated",
         "are finite trees of formulas\nthat are inductively generated"),
        ("  \\RightLabel{$\\delta_3$}\n  \\DeduceC{$!A_2$}\n  \\RightLabel{$R$}",
         "  \\RightLabel{$\\delta_3$}\n  \\DeduceC{$!A_3$}\n  \\RightLabel{$R$}"),
        ("The rules of \\Log{N2c} and \\Log{N2i}\nare given in \\olref{tab:N1}",
         "The rules of \\Log{N1c} and \\Log{N1i}\nare given in \\olref{tab:N1}"),
        ("$\\pheight{\\delta_1} = \\pheight{\\delta_2} = 1$.",
         "$\\pheight{\\delta_2} = \\pheight{\\delta_3} = 1$."),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
