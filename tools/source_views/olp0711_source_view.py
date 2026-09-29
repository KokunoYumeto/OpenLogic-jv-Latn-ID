"""Clarify the height edge count and repair the multiset-permutation example."""
def repaired_olp0711_source(s: str) -> str:
    repairs = (
        ("it is the maximal number of sequents between the\nend-sequent and an initial sequent.", "it is the maximal number of inference steps on a path between the\nend-sequent and an initial sequent."),
        (r"so $!D, !E \Sequent !E$ and $!E, !D \Sequent !D$ are the same", r"so $!D, !E \Sequent !E$ and $!E, !D \Sequent !E$ are the same"),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1
        s = s.replace(wrong, right, 1)
    return s
