"""Bounded comparison for sequent endpoint and valuation notation."""
from __future__ import annotations


def repaired_olp0403_source(text: str) -> str:
    repairs = (
        (
            r"!A_1, \dots, !A_n & \Sequent",
            r"!A_1, \dots, !A_m & \Sequent",
        ),
        (
            r"\pValue(!A)",
            r"\pValue v(!A)",
        ),
    )
    for old, new in repairs:
        assert text.count(old) == 1, (old, text.count(old))
        text = text.replace(old, new)
    return text
