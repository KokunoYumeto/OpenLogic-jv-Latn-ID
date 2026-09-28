"""Bounded Lindenbaum-proof repairs and localization of case prose."""


def repaired_olp0506_source(s: str) -> str:
    repairs = (
        (r"If $n>0$, we have to", r"For $n \ge 0$, we have to"),
        ("Let $n$ be the largest\n  of these.",
         "Choose $n$ at least as large as all these indices; if there are none, choose zero."),
        (r"""At
  each stage, at least one fewer disjunction $!B_i \lor !C_i$
  satisfies the conditions (since at each stage we add either $!B_i$
  or $!C_i$), so at some stage~$m$ we will have $j = i(m)$.""",
         r"""That disjunction remains eligible at every later stage until selected.
  At each earlier stage a disjunction $!B_i \lor !C_i$ with a smaller index
  is selected. There are only finitely many smaller indices, and each
  disjunction is selected at most once, since selection adds either $!B_i$
  or $!C_i$. Thus at some stage~$m$ we will have $j = i(m)$."""),
        (r"\text{if $\Gamma_n", r"\text{yen $\Gamma_n"),
        (r"\text{otherwise}", r"\text{yen ora}"),
    )
    for old, new in repairs:
        assert s.count(old) == 1
        s = s.replace(old, new, 1)
    return s
