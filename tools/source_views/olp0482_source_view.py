"""Bounded comparison view for the epistemic chapter's closing hook."""


def repaired_olp0482_source(s: str) -> str:
    assert s.count(r"\OLEndPartHook") == 1
    return s.replace(r"\OLEndPartHook", r"\OLEndChapterHook", 1)
