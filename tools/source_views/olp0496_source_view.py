"""Bounded comparison view for conjunction and proof grouping corrections."""


def repaired_olp0496_source(s: str) -> str:
    repairs = (
        (r"A construction of $!A_1 \land !A_1$", r"A construction of $!A_1 \land !A_2$"),
        (r"\UnaryInfC{$!A \lif (!A \lif \lfalse) \lif \lfalse$}",
         r"\UnaryInfC{$!A \lif ((!A \lif \lfalse) \lif \lfalse)$}"),
    )
    for old, new in repairs:
        assert s.count(old) == 1
        s = s.replace(old, new, 1)
    return s
