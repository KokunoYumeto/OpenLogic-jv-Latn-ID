"""Bounded comparison view for three BHK construction-variable errors."""


def repaired_olp0495_source(s: str) -> str:
    repairs = (
        (r"to constructions of~$C$)", r"to constructions of~$!C$)"),
        (r"function~$k_M$ from constructions", r"function~$k_{g,M}$ from constructions"),
        (r"it maps $M_1$ to $\tuple{1, M_2}$", r"it maps $M_1$ to $\tuple{1, M_1}$"),
    )
    for old, new in repairs:
        assert s.count(old) == 1
        s = s.replace(old, new, 1)
    return s
