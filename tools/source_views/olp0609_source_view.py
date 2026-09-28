"""Bounded comparison view for malformed membership in contradiction examples."""


def repaired_olp0609_source(s: str) -> str:
    repairs = (
        # OLPL-536: negation of A subset A union B concerns the same union.
        (r"    $\notin A \cup B$. So",
         r"    $x \notin A \cup B$. So"),
        (r"also $\in A \cup B$.", r"also $x \in A \cup B$."),
        (r"also $\in" + "\n" + r"    A \cup B$",
         r"also $x \in" + "\n" + r"    A \cup B$"),
        (r"that is $\notin C$.", r"that is $x \notin A \cup B$."),
        # OLPL-537: the transitivity witness remains x throughout.
        (r"is also $\in C$", r"is also $x \in C$"),
        (r"is $\notin C$.  Don't worry",
         r"is $x \notin C$.  Don't worry"),
        # OLPL-538: the first case concerns the same witness x.
        (r"$x \in A$ but $\notin B$.",
         r"$x \in A$ but $x \notin B$."),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
