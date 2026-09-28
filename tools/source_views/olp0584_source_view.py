"""Bounded cardinal-classification proof and explanatory-gloss repairs."""


def repaired_olp0584_source(s: str) -> str:
    repairs = (
        ("$A$ is not a natural number", "$A$ is not finite"),
        (
            r"By \olref{finitecardisoequal}, $\beta$",
            r"Since successors of finite ordinals are finite, $\beta$",
        ),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
