"""Normalize source-only English diaeresis for translated Javanese prose."""


def normalized_olp0581_source(s: str) -> str:
    wrong = r'na\"ively'
    assert s.count(wrong) == 1, s.count(wrong)
    return s.replace(wrong, "naively", 1)
