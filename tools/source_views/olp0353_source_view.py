"""Bounded comparison view for four primitive-recursion notation defects."""
from __future__ import annotations


def repaired_olp0353_source(text: str) -> str:
    repairs = (
        ("terms $G$ and $H$ that", "terms $G'$ and $H'$ that"),
        ("we want a term $H$ that", "we want a term $F$ that"),
        (r'h(z, f(x,\vec z), \vec z)', r'h(x, f(x,\vec z), \vec z)'),
        (r'F(\num{0}, \vec z) & \equiv G(\vec z)',
         r"F(\num{0}, \vec z) & \equiv G'(\vec z)"),
        (r'F(\overline{n+1}, \vec z) & \equiv H(',
         r"F(\overline{n+1}, \vec z) & \equiv H'("),
        (r'v(u,\vec z)', r'v(\vec z)'),
        (r'T(u) = \tuple{S((u)_0), H((u)_0,(u)_1)}',
         r'T(u) = \tuple{\fn{Succ}((u)_0), H((u)_0,(u)_1)}'),
    )
    for old, new in repairs:
        assert text.count(old) == 1, (old, text.count(old))
        text = text.replace(old, new)
    return text
