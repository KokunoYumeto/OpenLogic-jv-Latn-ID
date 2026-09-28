"""Bounded finite-support ordinal-exponentiation and citation repairs."""


def repaired_olp0579_source(s: str) -> str:
    repairs = (
        (
            "f\n" + r"\colon \alpha \to \beta",
            "f\n" + r"\colon \beta \to \alpha",
        ),
        (
            r"\Setabs{\gamma \in" + "\n" + r"\alpha}{f(\gamma) \neq 0}",
            r"\Setabs{\gamma \in" + "\n" + r"\beta}{f(\gamma) \neq 0}",
        ),
        (
            r"\Setabs{\gamma \in \alpha}{f(\gamma) \neq" + "\n" + r"g(\gamma)}",
            r"\Setabs{\gamma \in \beta}{f(\gamma) \neq" + "\n" + r"g(\gamma)}",
        ),
        (
            r"\citep[p.~199]{Potter2004}",
            r"\citep[kaca~199]{Potter2004}",
        ),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
