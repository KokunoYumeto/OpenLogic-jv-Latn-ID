"""Bounded comparison view for sublogic countermodel satisfaction notation."""
from __future__ import annotations


def repaired_olp0391_source(text: str) -> str:
    repairs = (
        (
            "$\\pAssign v\n  \\Entails[\\Log L] \\Gamma$",
            r"$\pSat{v}{\Gamma}[\Log L]$",
        ),
        (
            r"$\pAssign v \Entails/[\Log L] !B$",
            r"$\pSat/{v}{!B}[\Log L]$",
        ),
    )
    for old, new in repairs:
        assert text.count(old) == 1, (old, text.count(old))
        text = text.replace(old, new)
    return text
