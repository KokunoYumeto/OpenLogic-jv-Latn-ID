"""Bounded repairs to the product-rank citation and exercise formula."""


def repaired_olp0577_source(s: str) -> str:
    repairs = (
        (
            r"and invoke \olref{exranktuple}",
            r"and invoke \olref{exrankpow} twice and \olref{exrankcup}",
        ),
        (
            r"\setrank{A \times B}\max",
            r"\setrank{A \times B}=\max",
        ),
        (
            r"%\alpha \approx \alpha \ordplus 1$",
            r"%$\alpha \approx \alpha \ordplus 1$",
        ),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
