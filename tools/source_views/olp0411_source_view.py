"""Bounded comparison view for four substitution-source defects."""
from __future__ import annotations


def repaired_olp0411_source(text: str) -> str:
    repairs = (
        (r"\tagitem{prvIf}{\indcase{!A}{(!B \liff",
         r"\tagitem{prvIff}{\indcase{!A}{(!B \liff"),
        (r"\item \indcase{!A}{\Box !B}{%",
         r"\tagitem{prvBox}{\indcase{!A}{\Box !B}{%"),
        ("$}\n    " + r"\tagitem{prvDiamond}",
         "$}}{}\n    " + r"\tagitem{prvDiamond}"),
        (r"\Diamond(p_2 \lif p_3) & \Subst{\lif \Box(\Diamond(p_2 \lif p_3) \land p_2)}{\lnot\Box p_1}{p_2}",
         r"\Diamond(p_2 \lif p_3) & \lif \Subst{\Box(\Diamond(p_2 \lif p_3) \land p_2)}{\lnot\Box p_1}{p_2}"),
        (r"p_1 & \lif \Subst{\Box(p_1 \land \lnot\Box p_1)}{\Diamond(p_2 \lif p_3)}{p_1}",
         r"\Diamond(p_2 \lif p_3) & \lif \Subst{\Box(p_1 \land \lnot\Box p_1)}{\Diamond(p_2 \lif p_3)}{p_1}"),
    )
    for old, new in repairs:
        assert text.count(old) == 1, (old, text.count(old))
        text = text.replace(old, new)
    return text
