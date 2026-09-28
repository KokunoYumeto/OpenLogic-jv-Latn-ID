"""Bounded comparison view for three frozen-source currying defects."""
from __future__ import annotations


def repaired_olp0347_source(text: str) -> str:
    repairs = (
        (r'\olfileid{lam}{rep}{cur}', r'\olfileid{lam}{int}{cur}'),
        (r'M_1 \dots M_n \bredone\\', r'M_1 \dots M_n \\'),
        (r'\Subst{\Subst{P}{M_1}{x_1}\ldots}{M_n}{x_n}',
         r'\Subst{\Subst{N}{M_1}{x_1}\ldots}{M_n}{x_n}'),
    )
    for old, new in repairs:
        assert text.count(old) == 1, (old, text.count(old))
        text = text.replace(old, new)
    return text
