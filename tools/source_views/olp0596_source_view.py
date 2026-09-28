"""Bounded well-ordering/choice recursion and Hartogs-target repairs."""


def repaired_olp0596_source(s: str) -> str:
    repairs = (
        (r"\citeyear[p.~243]{Potter2004}", r"\citeyear[kaca~243]{Potter2004}"),
        (
            "Fix " + r"$A$" + ". By Choice, there is a choice function,",
            "Fix " + r"$A$" + ". The empty case is already well-ordered; otherwise, by Choice there is a choice function,",
        ),
        (r"$\delta \leq \alpha$", r"$\delta \geq \alpha$"),
        (
            r"\text{if }A = \funimage{g}{\alpha}",
            r"\text{if }A \subseteq \funimage{g}{\alpha}",
        ),
        (
            "So " + r"$g$" + " is\n!!{injective}.",
            "So the pre-stop restriction of " + r"$g$" + " is\n!!{injective}.",
        ),
        (
            r"$\cardless{\alpha}{\Pow{A} \setminus \{\emptyset\}}$",
            r"$\cardle{\alpha}{A}$",
        ),
        (r"i.e.\ that", "i.e. that"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
