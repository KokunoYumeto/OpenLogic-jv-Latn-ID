"""Bounded semantic comparison view for Curry--Howard introductory prose."""


def repaired_olp0686_source(s: str) -> str:
    repairs = (
        ("typing rule for composition\nterms", "typing rule for application\nterms"),
        ("(the result of replacing every free occurrence of $x$ in~$N$ by $M$).",
         "(the result of replacing every free occurrence of $x$ in~$N$ by $M$,\n"
         "renaming bound variables first when needed to avoid capturing free variables)."),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
