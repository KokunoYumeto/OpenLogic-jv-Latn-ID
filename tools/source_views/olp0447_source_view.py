"""Bounded truth-lemma source comparison view; frozen source stays untouched."""


def repaired_olp0447_source(s: str) -> str:
    old_ref = r"\olref[mod]{prop:diamond},}{} for some"
    new_ref = r"\olref[mod]{lem:box-iff-diamond},}{} for some"
    assert s.count(old_ref) == 1
    s = s.replace(old_ref, new_ref, 1)
    old_tag = "probNot,proband,probOr"
    new_tag = "probNot,probAnd,probOr"
    assert s.count(old_tag) == 1
    return s.replace(old_tag, new_tag, 1)
