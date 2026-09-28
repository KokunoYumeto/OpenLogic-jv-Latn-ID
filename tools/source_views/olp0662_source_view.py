"""Bounded comparison view for three grafting-example source slips."""


def repaired_olp0662_source(s: str) -> str:
    repairs = (
        (r"\UnaryInfC{$!B \lif !C$}",
         r"\UnaryInfC{$!B \lif !A$}"),
        (r"\Log{N1c}-!!{proof} (\Log{N1i}-!!{proof}) of~$\Gamma_2 \Sequent !B$",
         r"\Log{N2c}-!!{proof} (\Log{N2i}-!!{proof}) of~$\Gamma_2 \Sequent !B$"),
        (r"\pheight{\delta}$", r"\pheight{\delta_1}$"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
