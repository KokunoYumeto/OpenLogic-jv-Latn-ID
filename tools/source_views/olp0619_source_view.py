"""Bounded comparison view for two literal-letter b notation slips."""


def repaired_olp0619_source(s: str) -> str:
    repairs = (
        (r"$\mathrm{a} \sqsubseteq b$",
         r"$\mathrm{a} \sqsubseteq \mathrm{b}$"),
        (r"r_1 & = \mathrm{a} \circ b \text{ and}",
         r"r_1 & = \mathrm{a} \circ \mathrm{b} \text{ and}"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
