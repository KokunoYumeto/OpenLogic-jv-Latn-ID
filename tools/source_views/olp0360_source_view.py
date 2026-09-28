"""Bounded comparison view for the free-variable section's chapter and scope."""
from __future__ import annotations


def repaired_olp0360_source(text: str) -> str:
    repairs = (
        ('% Chapter: introduction', '% Chapter: syntax'),
        (r'the corresponding' + '\n' + r'occurrence of~$N$ is the \emph{scope}',
         r'the corresponding' + '\n' + r'occurrence of~$M$ is the \emph{scope}'),
    )
    for old, new in repairs:
        assert text.count(old) == 1, (old, text.count(old))
        text = text.replace(old, new)
    return text
