"""Use the actual multiset objects in the union explanation."""
def repaired_olp0700_source(s: str) -> str:
    wrong = "multiset union of the two sequences"
    assert s.count(wrong) == 1
    return s.replace(wrong, "multiset union of the two multisets", 1)
