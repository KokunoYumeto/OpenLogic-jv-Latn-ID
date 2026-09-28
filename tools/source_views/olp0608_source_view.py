"""Bounded comparison view for the extra parenthesis in Example 2."""


def repaired_olp0608_source(s: str) -> str:
    wrong = r"$C \subseteq (A \cup (C \setminus A)$"
    right = r"$C \subseteq A \cup (C \setminus A)$"
    assert s.count(wrong) == 1, s.count(wrong)
    return s.replace(wrong, right, 1)
