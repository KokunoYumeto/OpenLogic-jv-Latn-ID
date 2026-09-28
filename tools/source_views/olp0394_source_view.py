"""Bounded comparison for Łukasiewicz conjunction, exercise and modal value."""
from __future__ import annotations


def repaired_olp0394_source(text: str) -> str:
    repairs = (
        (
            "  \\item The standard propositional language $\\Lang L_0$ with\n"
            "  $\\lnot$, $\\land$, $\\lor$, $\\lif$.",
            "  \\item The standard propositional language $\\Lang L_0$ with\n"
            "  $\\lfalse$, $\\lnot$, $\\land$, $\\lor$, $\\lif$.",
        ),
        (
            "  \\item Truth functions are given by the following tables:",
            "  \\item For the propositional constant, "
            "$\\tf{\\lfalse}[\\LogLuk[3]] = \\False$. "
            "The remaining truth functions are given by the following tables:",
        ),
        (
            "\\[\\tf{\\land}(\\False, \\Undef) =\n\\tf{\\land}(\\False, \\Undef) = \\False.\\]",
            "\\[\\tf{\\land}(\\False, \\Undef) =\n\\tf{\\land}(\\Undef, \\False) = \\False.\\]",
        ),
        (
            r"$(\lnot p \land p) \lif q)$",
            r"$((\lnot p \land p) \lif q)$",
        ),
        (
            "\\pValue v(\\lnot \\Diamond(p \\land \\lnot p)) =\n\\Undef$",
            "\\pValue v(\\lnot \\Diamond(p \\land \\lnot p)) =\n\\False$",
        ),
    )
    for old, new in repairs:
        assert text.count(old) == 1, (old, text.count(old))
        text = text.replace(old, new)
    return text
