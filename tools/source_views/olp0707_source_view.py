"""Restore the explicit multiset separator in the G3c universal-left premise."""
def repaired_olp0707_source(s: str) -> str:
    wrong = r"\Axiom$ !A(t), \lforall[x][!A(x)]\Gamma \fCenter \Delta$"
    right = r"\Axiom$ !A(t), \lforall[x][!A(x)], \Gamma \fCenter \Delta$"
    assert s.count(wrong) == 1
    return s.replace(wrong, right, 1)
