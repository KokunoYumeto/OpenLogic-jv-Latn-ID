"""Bounded comparison view for arity and undefined-case application."""
from __future__ import annotations


def repaired_olp0348_source(text: str) -> str:
    repairs = (
        (r'an $n$-ary partial function from $\Nat$' + '\n' + r'to $\Nat$.',
         r'a $k$-ary partial function from $\Nat$' + '\n' + r'to $\Nat$.'),
        (r'$F, \num{n_0}\, \num{n_1}',
         r'$F\, \num{n_0}\, \num{n_1}'),
    )
    for old, new in repairs:
        assert text.count(old) == 1, (old, text.count(old))
        text = text.replace(old, new)
    return text
