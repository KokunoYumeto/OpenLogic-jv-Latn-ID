"""Bounded comparison for tautological-instance proof repairs and annotations."""
from __future__ import annotations


def repaired_olp0416_source(text: str) -> str:
    repairs = (
        (r"\tagitem{prvFalse}{\indcase{!A}{\lnot !B}",
         r"\tagitem{prvNot}{\indcase{!A}{\lnot !B}"),
        (r"\text{by definition of $\pSat{v}{}$}.",
         r"\text{by definition of $\mSat{M}{}[w]$}."),
        (r"\pSat{v}{!B \lif !C} \Leftrightarrow {} &",
         r"\pSat{v}{!B \liff !C} \Leftrightarrow {} &"),
    )
    for old, new in repairs:
        assert text.count(old) == 1, (old, text.count(old))
        text = text.replace(old, new)
    annotations = (
        (r"\text{by definition of", r"\text{miturut definisi"),
        (r"\text{by assumption}", r"\text{miturut asumsi}"),
        (r"\text{by induction hypothesis}", r"\text{miturut hipotesis induksi}"),
        (r"\text{since ", r"\text{amarga "),
        (r"\text{ and }", r"\text{ lan }"),
        (r"\text{ or }", r"\text{ utawa }"),
        (r"\text{or }", r"\text{utawa }"),
        (r"\text{either }", r"\text{salah siji: }"),
    )
    for old, new in annotations:
        assert text.count(old) > 0, old
        text = text.replace(old, new)
    return text
