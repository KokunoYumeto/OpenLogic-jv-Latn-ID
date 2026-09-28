"""Bounded comparison view for regular minimization's search functional."""
from __future__ import annotations


def repaired_olp0380_source(text: str) -> str:
    repairs = (
        (r"To !!{lambda define}~$h$", r"To !!{lambda define}~$g$"),
        (
            r"\fn{IsZero} (f\, \vec{x}\, y)\, y\, (g\, \vec{x} (\fn{Succ}\, y)]]",
            r"\fn{IsZero} (f\, \vec{x}\, y)\, y\, (g\, f\, \vec{x} (\fn{Succ}\, y))]]",
        ),
        (r"\num{h(n_1, \dots, n_k)}", r"\num{g(n_1, \dots, n_k)}"),
    )
    for old, new in repairs:
        assert text.count(old) == 1, (old, text.count(old))
        text = text.replace(old, new)
    return text
