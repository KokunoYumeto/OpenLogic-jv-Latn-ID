"""Respect the closed-term instance convention stated in rules-proofs."""
from olp0703_source_view import repaired_olp0703_source
def repaired_olp0703_source_v185(s: str) -> str:
    s = repaired_olp0703_source(s)
    wrong = "$t$~is a term not containing any"
    assert s.count(wrong) == 1
    return s.replace(wrong, "$t$~is a closed term not containing any", 1)
