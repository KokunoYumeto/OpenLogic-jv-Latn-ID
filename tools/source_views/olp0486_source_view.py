"""Bounded source comparison for epistemic truth clauses and display localization.

The frozen English remains unchanged. The first three replacements repair the
negation and conditional truth clauses and their malformed satisfaction macros.
The last two normalize English inside the displayed equation for target-language
math-sequence comparison only.
"""


def repaired_olp0486_source(s: str) -> str:
    old_not = (r"\tagitem{prvNot}{\indcase{!A}{\lnot !B}{$\mSat{M}{\indfrm}[w]$ iff"
               "\n" r"    $\mSat/{M}{!B}[w]$}.}{}")
    new_not = (r"\tagitem{prvNot}{\indcase{!A}{\lnot !B}{$\mSat{M}{\indfrm}[w]$ iff"
               "\n" r"    not $\mSat{M}{!B}[w]$}.}{}")
    old_if = (r"\tagitem{prvIf}{\indcase{!A}{(!B \lif !C)}{$\mSat{M}{\indfrm}[w]$ iff"
              "\n" r"    $\mSat/{M}{!B}[w]$ or $\mSat{M}{!C}[w]$}.}{}")
    new_if = (r"\tagitem{prvIf}{\indcase{!A}{(!B \lif !C)}{$\mSat{M}{\indfrm}[w]$ iff"
              "\n" r"    not $\mSat{M}{!B}[w]$ or $\mSat{M}{!C}[w]$}.}{}")
    assert s.count(old_not) == s.count(old_if) == 1
    s = s.replace(old_not, new_not, 1).replace(old_if, new_if, 1)
    assert s.count(r"\mSat/{M}") == 0
    assert s.count(r"\intertext{where}") == 1
    assert s.count(r"\text{ and}") == 1
    return s.replace(r"\intertext{where}", r"\intertext{ing kene}", 1).replace(
        r"\text{ and}", r"\text{ lan}", 1
    )
