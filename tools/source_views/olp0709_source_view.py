"""Give LK its own label and include its fourth displayed sequence context."""
def repaired_olp0709_source(s: str) -> str:
    repairs = (
        (r"\ollabel{tab:G1c}", r"\ollabel{tab:LK}"),
        (r"conclusion sequent. $\Gamma$, $\Delta$, and~$\Pi$ are", r"conclusion sequent. $\Gamma$, $\Delta$, $\Pi$, and~$\Lambda$ are"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1
        s = s.replace(wrong, right, 1)
    return s
