"""Bounded comparison for LP proof notation and conjunction induction."""
from __future__ import annotations


def repaired_olp0397_source(text: str) -> str:
    repairs = (
        (
            "\\pValue\n  v[\\LogKs](!A)",
            "\\pValue\n  v(!A)[\\LogKs]",
        ),
        (
            r"\pValue{v'}[\LogCL](!A)",
            r"\pValue{v'}(!A)[\LogCL]",
        ),
        (
            r"\pValue v(!B)[\LogKs]  =" "\n"
            r"      \False$ or $\pValue v(!B)[\LogKs]  =",
            r"\pValue v(!B)[\LogKs]  =" "\n"
            r"      \False$ or $\pValue v(!C)[\LogKs]  =",
        ),
        (
            r"\pValue v(!B)[\LogKs]  =" "\n"
            r"      \True$ and $\pValue v(!B)[\LogKs]  =",
            r"\pValue v(!B)[\LogKs]  =" "\n"
            r"      \True$ and $\pValue v(!C)[\LogKs]  =",
        ),
    )
    for old, new in repairs:
        assert text.count(old) == 1, (old, text.count(old))
        text = text.replace(old, new)
    return text
