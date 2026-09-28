"""Bounded comparison view for permutation-conversion source slips."""


def repaired_olp0675_source(s: str) -> str:
    wrong = "$!A \\ident !B \\lor !C$"
    right = "$!A \\ident !B \\land !C$"
    assert s.count(wrong) == 1
    s = s.replace(wrong, right, 1)
    assert s.count(r"\Elim{\exists}") == 2
    s = s.replace(r"\Elim{\exists}", r"\Elim{\lexists}")
    return s
