"""Bounded comparison view for public-announcement semantic corrections."""


def repaired_olp0490_source(s: str) -> str:
    old_not = (r"\tagitem{prvNot}{\indcase{!A}{\lnot !B}{$\mSat{M}{\indfrm}[w]$ iff"
               "\n" r"    $\mSat/{M}{!B}[w]$}.}{}")
    new_not = (r"\tagitem{prvNot}{\indcase{!A}{\lnot !B}{$\mSat{M}{\indfrm}[w]$ iff"
               "\n" r"    not $\mSat{M}{!B}[w]$}.}{}")
    old_if = (r"\tagitem{prvIf}{\indcase{!A}{(!B \lif !C)}{$\mSat{M}{\indfrm}[w]$ iff"
              "\n" r"    $\mSat/{M}{!B}[w]$ or $\mSat{M}{!C}[w]$}.}{}")
    new_if = (r"\tagitem{prvIf}{\indcase{!A}{(!B \lif !C)}{$\mSat{M}{\indfrm}[w]$ iff"
              "\n" r"    not $\mSat{M}{!B}[w]$ or $\mSat{M}{!C}[w]$}.}{}")
    old_announcement = r"$[!A]B$"
    new_announcement = r"$[!A] !B$"
    old_model_claim = "are the same model."
    new_model_claim = "are not the same model; the latter also omits the upper world."
    assert s.count(old_not) == s.count(old_if) == 1
    assert s.count(old_announcement) == s.count(old_model_claim) == 1
    s = (s.replace(old_not, new_not, 1)
         .replace(old_if, new_if, 1)
         .replace(old_announcement, new_announcement, 1)
         .replace(old_model_claim, new_model_claim, 1))
    assert r"\mSat/{M}" not in s
    return s
