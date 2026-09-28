"""Bounded comparison view for OLP-0426 standard-translation defects."""


def repaired_olp0426_source(s: str) -> str:
    old = "% Chapter: frame-correspondence"
    new = "% Chapter: frame-definability"
    assert s.count(old) == 1
    s = s.replace(old, new, 1)

    old = r"\tagitem{prvTrue}{\indcase{!A}{\lfalse}{$\ST_x(\indfrm) = \ltrue$.}}{}"
    new = r"\tagitem{prvTrue}{\indcase{!A}{\ltrue}{$\ST_x(\indfrm) = \ltrue$.}}{}"
    assert s.count(old) == 1
    s = s.replace(old, new, 1)

    old = r"\liff \ST_x(!C))}$.}{}"
    new = r"\liff \ST_x(!C))$.}{}"
    assert s.count(old) == 1
    s = s.replace(old, new, 1)
    return s
