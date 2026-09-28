"""Bounded Hartogs proof variable, relation, codomain and cardinal-law repairs."""


def repaired_olp0595_source(s: str) -> str:
    repairs = (
        (r"$B \subseteq R$", r"$B \subseteq A$"),
        (
            r"\Setabs{\tuple{f(\alpha), f(\beta)} \in A \times A}{\alpha \in \beta}",
            r"\Setabs{\tuple{f(\xi), f(\zeta)}}{\xi,\zeta\in\alpha \land \xi\in\zeta}",
        ),
        (r"\to \tuple{A, R}$", r"\to A$"),
        (r"\to \tuple{B, S}$", r"\to B$"),
        (
            r"$\cardeq{\cardeq{A \disjointsum B}{A \times" + "\n" + r"B}}{M}$",
            r"$\cardeq{A \disjointsum B}{M}$" + " and "
            + r"$\cardeq{A \times B}{M}$",
        ),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
