"""Exclude logical constants from the structural necessity examples."""
from olp0699_source_view import repaired_olp0699_source
def repaired_olp0699_source_v182(s: str) -> str:
    s = repaired_olp0699_source(s)
    wrong = "For distinct atomic schematic formulas, contraction"
    assert s.count(wrong) == 1
    return s.replace(wrong, "For distinct predicate-atomic schematic formulas, contraction", 1)
