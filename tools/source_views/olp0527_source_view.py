"""Repair the second-premise truth assertion in the transitivity countermodel."""


def repaired_olp0527_source(s: str) -> str:
    repairs = (
        (r"$\mSat/{M}{q \lif r}$ is true at all worlds in it",
         r"$q \lif r$ is true at all worlds in it"),
        (r"However, the $p$-admitting sphere", r"However, the only $p$-admitting sphere"),
        (r"r}[w_2]$." + "\n" + r"\end{ex}",
         r"r}[w_2]$. Thus the counterfactual conclusion is false at the center." + "\n" + r"\end{ex}"),
    )
    for old, new in repairs:
        assert s.count(old) == 1, old
        s = s.replace(old, new, 1)
    return s
