"""Bounded comparison view for normalization-introduction source slips."""


def repaired_olp0672_source(s: str) -> str:
    repairs = (
        ("Your\n!!{proof}~$\\delta_1$ of~$!A \\lif !B$",
         "Your\n!!{proof} of~$!A \\lif !B$"),
        ("\\AxiomC{}\n\\RightLabel{$\\delta_2$}\n\\DeduceC{$!A$}",
         "\\AxiomC{}\n\\RightLabel{$\\delta_1$}\n\\DeduceC{$!A$}"),
        ("The\nsub-!!{formula} property, that you can always !!{prove} a result using\n"
         "only sub-!!{formula}s of the result in your !!{proof}, follows from\n"
         "normalization for natural deduction just as it follows from\n"
         "cut-elimination for the sequent calculus.",
         "For intuitionistic natural deduction, the\n"
         "sub-!!{formula} property, that you can always !!{prove} a result using\n"
         "only sub-!!{formula}s of undischarged assumptions or the result in your\n"
         "!!{proof}, follows from normalization just as it follows from\n"
         "cut-elimination for the sequent calculus."),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
