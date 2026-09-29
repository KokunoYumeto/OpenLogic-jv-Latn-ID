"""Correct the mG3i separator, matching minimal variant and table identity."""
def repaired_olp0710_source(s: str) -> str:
    repairs = (
        (r"\Axiom$ !A(t), \lforall[x][!A(x)]\Gamma \fCenter \Delta$", r"\Axiom$ !A(t), \lforall[x][!A(x)], \Gamma \fCenter \Delta$"),
        ("\\Log{mG1m} is\n\\Log{mG1i}", "\\Log{mG3m} is\n\\Log{mG3i}"),
        (r"\ollabel{tab:G3c}", r"\ollabel{tab:mG3i}"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, wrong
        s = s.replace(wrong, right, 1)
    return s
