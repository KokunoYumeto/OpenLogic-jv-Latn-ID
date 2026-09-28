"""Bounded comparison view for the two Church-numeral subscripts."""
from __future__ import annotations


def repaired_olp0349_source(text: str) -> str:
    old = r'$X \num m_0 \ldots \num' + '\n' + r'm_{n-1}$'
    new = r'$X \num{m_0} \ldots \num{m_{n-1}}$'
    assert text.count(old) == 1, text.count(old)
    return text.replace(old, new)
