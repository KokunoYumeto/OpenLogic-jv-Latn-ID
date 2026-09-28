"""Bounded comparison view for the temporal chapter's closing hook."""


def repaired_olp0476_source(s: str) -> str:
    assert s.count(r"\OLEndPartHook") == 1
    return s.replace(r"\OLEndPartHook", r"\OLEndChapterHook", 1)
