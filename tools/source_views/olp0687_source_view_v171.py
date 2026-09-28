"""Scope normalization to well-typed terms; retain the earlier audited view."""
from olp0687_source_view import repaired_olp0687_source

def repaired_olp0687_source_v171(s: str) -> str:
    s = repaired_olp0687_source(s)
    repairs = (
        ("we show that every proof term", "we show that every well-typed proof term"),
        ("All proof terms reduce to normal form", "All well-typed proof terms reduce to normal form"),
        ("where $M$ is a proof term.", "where $M$ is a well-typed proof term."),
    )
    for wrong, right in repairs:
        assert s.count(wrong) == 1
        s = s.replace(wrong, right, 1)
    return s
