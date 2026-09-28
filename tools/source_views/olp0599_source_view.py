"""Bounded Banach--Tarski dimension, tangent and citation repairs."""


def repaired_olp0599_source(s: str) -> str:
    repairs = (
        (
            "Any ball can be decomposed into finitely many pieces",
            "Any three-dimensional ball can be decomposed into finitely many pieces",
        ),
        (
            r"$\tan(\pi(r-\nicefrac{1}{2})))$",
            r"$\tan(\pi(r-\nicefrac{1}{2}))$",
        ),
        (
            r"\citet[Theorem 3.12]{Wagon2016}",
            r"\citet[Téoréma 3.12]{Wagon2016}",
        ),
        (
            r"\citet[pp.~66--7]{Wagon2016}",
            r"\citet[kaca~66--7]{Wagon2016}",
        ),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
