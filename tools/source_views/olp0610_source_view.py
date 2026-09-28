"""Bounded comparison view for three reading-proofs example slips."""


def repaired_olp0610_source(s: str) -> str:
    repairs = (
        # OLPL-539: (b) is the reverse inclusion, as the proof itself says.
        (r"and (b) $A \cap (A \cup B)" + "\n" + r"  \subseteq A$.",
         r"and (b) $A \subseteq A \cap (A \cup B)$."),
        # OLPL-540: one stray parenthesis is inside the final inline formula.
        (r"$z" + "\n" + r"  \in A \cup B)$, i.e., (2)",
         r"$z" + "\n" + r"  \in A \cup B$, i.e., (2)"),
        # OLPL-541: the exercise's final membership needs the element z.
        (r"is also $\in A \cup (A" + "\n" + r"  \cap B)$.",
         r"is also $z \in A \cup (A" + "\n" + r"  \cap B)$."),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
