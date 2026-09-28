"""Bounded comparison for infinite-valued Łukasiewicz falsity constant."""
from __future__ import annotations


def repaired_olp0400_source(text: str) -> str:
    repairs = (
        (
            "  \\item The standard propositional language $\\Lang L_0$ with\n"
            "  $\\lnot$, $\\land$, $\\lor$, $\\lif$.",
            "  \\item The standard propositional language $\\Lang L_0$ with\n"
            "  $\\lfalse$, $\\lnot$, $\\land$, $\\lor$, $\\lif$.",
        ),
        (
            "  \\item Truth functions are given by the following functions:",
            "  \\item For the falsity constant, "
            "$\\tf{\\lfalse}[\\LogLuk[\\infty]] = 0$. "
            "Other truth functions are given by the following functions:",
        ),
    )
    for old, new in repairs:
        assert text.count(old) == 1, (old, text.count(old))
        text = text.replace(old, new)
    return text
