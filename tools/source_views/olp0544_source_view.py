"""Normalize an English TeX diaeresis only for OLP-0544 comparison."""


def normalized_olp0544_source(s: str) -> str:
    old = r'na\"ively'
    assert s.count(old) == 1, s.count(old)
    return s.replace(old, 'naively', 1)
