"""Bounded comparison view for nonempty proper initial segments."""


def repaired_olp0618_source(s: str) -> str:
    wrong = "segment of a string~$t$ of symbols is any string~$s$ that agrees"
    right = "segment of a string~$t$ of symbols is any nonempty string~$s$ that agrees"
    assert s.count(wrong) == 1, s.count(wrong)
    return s.replace(wrong, right, 1)
