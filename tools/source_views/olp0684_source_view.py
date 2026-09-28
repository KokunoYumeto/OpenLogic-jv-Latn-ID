"""Bounded comparison view for the signed-tableau example and copy edits."""


def repaired_olp0684_source(s: str) -> str:
    repairs = (
        (r"\sFmla{\False}{!C}, \sFmla{\True}{!D}$",
         r"\sFmla{\False}{!C}, \sFmla{\False}{!D}$"),
        ("shows that would show that", "shows that"),
        ("a\nclause tableau for", "a\nclosed tableau for"),
        (r"$\sFmla{\True}{!A}$ and $\sFmla{\False}{!A}$. If every branch is",
         r"$\sFmla{\True}{!A}$ and $\sFmla{\False}{!A}$, or contains $\sFmla{\True}{\lfalse}$. If every branch is"),
        ("already occur on the branch.\n\nIf this proof search",
         "already occur on the branch. If no applicable unused term exists,\n"
         "this rule adds no node at that stage; reconsider it when new terms\n"
         "become available.\n\nIf this proof search"),
        ("contains a finite open branch where all non-atomic !!{formula}s are\n"
         "checked off, or the search produces an infinite, finitely branching",
         "contains a finite open branch where all checkable non-atomic !!{formula}s\n"
         "are checked off and all applicable term instances of the unchecked\n"
         "quantified formulas are present, or the search produces an infinite, finitely branching"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1, (wrong, s.count(wrong))
        s = s.replace(wrong, right, 1)
    return s
