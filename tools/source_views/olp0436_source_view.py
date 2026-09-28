"""Bounded comparison view restoring the omitted axiom cases in soundness induction."""


def repaired_olp0436_source(s: str) -> str:
    old = ("If\n    $!B$ is a tautological instance or an instance of one of $!A_1$,\n"
           "    \\dots, $!A_n$, we proceed as in the previous step.")
    new = ("If\n    $!B$ is a tautological instance, an instance of~\\Ax{K},"
           "\\iftag{prvDiamond}{ or of~\\Dual{},}{} or an instance of one of $!A_1$,\n"
           "    \\dots, $!A_n$, we proceed as in the previous step.")
    assert s.count(old) == 1
    return s.replace(old, new, 1)
