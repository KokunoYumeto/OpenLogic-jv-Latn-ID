"""Bounded comparison view for defects in the inference-patterns lesson."""


def repaired_olp0606_source(s: str) -> str:
    repairs = (
        # OLPL-532: both conclusions require the element already quantified.
        (r"is also $\in D$ (c)", r"is also $x \in D$ (c)"),
        (r"is" + "\n" + r"  also $\in E$ (d)", r"is" + "\n" + r"  also $x \in E$ (d)"),
        # OLPL-533: incomplete membership expressions in the existential explanation.
        (r"other than that it is" + "\n" + r"$\in A$",
         r"other than that it is" + "\n" + r"in $A$"),
        (r"is also $\in \emptyset$ and every",
         r"is also $x \in \emptyset$ and every"),
        (r"is also $\in A$. Negating", r"is also $x \in A$. Negating"),
        (r"is $\notin \emptyset$ or some", r"is $x \notin \emptyset$ or some"),
        (r"is $\notin A$. Since", r"is $x \notin A$. Since"),
        (r"nothing is $\in \emptyset$", r"nothing is $x \in \emptyset$"),
        (r"things~$\in A$", r"things in~$A$"),
        # OLPL-534: the equivalence concerns the set A, not a witness x.
        (r"So $x \neq" + "\n" + r"    \emptyset$ iff",
         r"So $A \neq" + "\n" + r"    \emptyset$ iff"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
