"""Bounded comparison view for the composition representation display."""


def repaired_olp0647_source(s: str) -> str:
    repairs = (
        (r"\dots \land !A_{g_{k-1}}(x_0,\dots,x_{l-1},z_{k-1}) \land]]\\",
         r"\dots \land !A_{g_{k-1}}(x_0,\dots,x_{l-1},z_{k-1}) \land\\"),
        (r"!A_f(z_0,\dots,z_{k-1},y)).",
         r"!A_f(z_0,\dots,z_{k-1},y))]]."),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
