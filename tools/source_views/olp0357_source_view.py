"""Bounded comparison view for the fully parenthesized exercise term."""
from __future__ import annotations


def repaired_olp0357_source(text: str) -> str:
    old = (r'$(\lambd[g][(\lambd[x][(g (x x))])' + '\n'
           + r'  (\lambd[x][(g (x x))])])$')
    new = (r'$(\lambd[g][((\lambd[x][(g (x x))])' + '\n'
           + r'  (\lambd[x][(g (x x))]))])$')
    assert text.count(old) == 1, text.count(old)
    return text.replace(old, new)
