"""Bounded comparison view for midsequent proof references and base case."""


def repaired_olp0661_source(s: str) -> str:
    repairs = (
        (r"inferences in~$\pi_1'$. That's because",
         r"inferences in~$\pi_1$. That's because"),
        ("Since all quantifier inferences\n  have one premise, there is a single topmost quantifier inference.\n  Its premise is the midsequent.",
         "Since all quantifier inferences\n  have one premise, if any exists there is a single topmost quantifier inference whose premise is the midsequent. If none exists, the end-sequent itself is the midsequent."),
        (r"\UnaryInf$!\Gamma' \fCenter \Delta', \lexists[x][!A(x)], !B$",
         r"\UnaryInf$\Gamma' \fCenter \Delta', \lexists[x][!A(x)], !B$"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
