"""Bounded proof comparison view for complete consistent set properties."""


def repaired_olp0443_source(s: str) -> str:
    fixes = (
        (
            r"if $!A \notin \Gamma$ then $!A \in \Gamma$",
            r"if $!A \notin \Gamma$ then $\lnot !A \in \Gamma$",
        ),
        (
            "a contradiction.}}{}",
            ("a contradiction. Conversely, if $!A \\in \\Gamma$ or $!B \\in \\Gamma$, "
             "then $!A \\lor !B \\in \\Gamma$ by deductive closure, since "
             "$!A \\lif (!A \\lor !B)$ and $!B \\lif (!A \\lor !B)$ "
             "are tautological instances.}}{}"),
        ),
        (
            r"Conversely, suppose $!A \lif !B \notin \Gamma$.",
            r"Conversely, suppose $!A \liff !B \notin \Gamma$.",
        ),
        (
            "So neither $!A \\in \\Gamma$ and $!B \\in \\Gamma$, nor $!A \\notin",
            ("If neither is in the set, completeness puts both negations in it. "
             "The tautological instance $\\lnot !A \\lif (\\lnot !B \\lif (!A \\liff !B))$ "
             "and deductive closure then put the biconditional in the set, a contradiction. "
             "So neither $!A \\in \\Gamma$ and $!B \\in \\Gamma$, nor $!A \\notin"),
        ),
    )
    for old, new in fixes:
        assert s.count(old) == 1
        s = s.replace(old, new, 1)
    return s
