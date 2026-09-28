"""Bounded Reflection-proof notation repairs and citation-locator localization."""


def repaired_olp0572_source(s: str) -> str:
    changes = (
        (
            r'\phi_i(\overline{a}_i, x))',
            r'\phi_i(\overline{a}_i, x)',
        ),
        (
            r'S &= \bigcup_{m < \omega} S_n.',
            r'S &= \bigcup_{m < \omega} S_m.',
        ),
        (
            r'\Setabs{y}{(\exists x \in A)\phi(x,y}',
            r'\Setabs{y}{(\exists x \in A)\phi(x,y)}',
        ),
        (
            '\\citet[first\npart of Theorem 2]{Levy1960}',
            '\\citet[bagéan kapisan Teorema 2]{Levy1960}',
        ),
        (
            r'\citet[Theorem 6]{Levy1960}',
            r'\citet[Teorema 6]{Levy1960}',
        ),
    )
    for wrong, right in changes:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
